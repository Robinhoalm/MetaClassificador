import os
import json
import argparse
from time import sleep
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from sklearn.metrics import accuracy_score, classification_report


def load_data(path):
    df = pd.read_csv(path)
    # Try to detect common column names
    if 'text' in df.columns:
        texts = df['text']
    elif 'tweet' in df.columns:
        texts = df['tweet']
    elif 'content' in df.columns:
        texts = df['content']
    elif 'text_clean' in df.columns:
        texts = df['text_clean']
    elif 'airline_sentiment' in df.columns:
        texts = df['text']
    else:
        # fallback to first string-like column
        for c in df.columns:
            if df[c].dtype == object:
                texts = df[c]
                break

    # Attempt to find label column
    label_cols = ['sentiment', 'label', 'airline_sentiment', 'target']
    label = None
    for c in label_cols:
        if c in df.columns:
            label = df[c]
            break

    if label is None:
        raise RuntimeError('Não foi possível encontrar automaticamente a coluna de rótulo. Verifique o CSV.')

    return pd.DataFrame({'text': texts, 'label': label})


def classify_with_gpt(client, texts, batch_size=1, pause_s=1.0):
    preds = []
    confidences = []
    justifications = []
    for i, t in enumerate(texts):
        prompt = (
            "Classifique o sentimento deste texto em uma das três opções: Positive, Negative, Neutral.\n"
            f"Texto: \"{t}\"\n"
            "Responda única e exclusivamente em formato JSON com as chaves: \"label\" (uma das opções), \"confidence\" (valor float entre 0 e 1) e \"justification\" (1-2 frases justificando a escolha)."
        )

        try:
            resp = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": "Você é um classificador de sentimento que responde estritamente em JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )

            text = resp.choices[0].message.content.strip()
            # Try parse JSON
            parsed = json.loads(text)
            label = parsed.get('label')
            conf = float(parsed.get('confidence', 0))
            just = parsed.get('justification', '')
        except Exception:
            # fallback: try to extract label words
            text_lower = text.lower() if 'text' in locals() else ''
            if 'positive' in text_lower or 'positivo' in text_lower:
                label = 'Positive'
            elif 'negative' in text_lower or 'negativo' in text_lower:
                label = 'Negative'
            else:
                label = 'Neutral'
            conf = 0.0
            just = ''

        preds.append(label)
        confidences.append(conf)
        justifications.append(just)

        if (i + 1) % batch_size == 0:
            sleep(pause_s)

    return preds, confidences, justifications



def main():
    parser = argparse.ArgumentParser(description='Baixa/avalia dataset do Kaggle e classifica com GPT-4.1-nano')
    parser.add_argument('--csv', type=str, default='data/airline_sentiment.csv', help='Caminho para CSV do dataset')
    parser.add_argument('--sample', type=int, default=200, help='Número de amostras para avaliação (para economizar tokens)')
    args = parser.parse_args()

    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise RuntimeError('Defina OPENAI_API_KEY no seu ambiente (.env não versionado) antes de rodar.')

    # check csv exists
    if not os.path.exists(args.csv):
        print('Arquivo CSV não encontrado em', args.csv)
        print('Para baixar do Kaggle, instale o kaggle-cli e rode:')
        print('  kaggle datasets download -d crowdflower/twitter-airline-sentiment -p data --unzip')
        return

    df = load_data(args.csv)

    # normalize labels to English words
    df['label_norm'] = df['label'].astype(str).str.lower().map(lambda v: 'Positive' if 'pos' in v else ('Negative' if 'neg' in v else 'Neutral'))

    sample = df.sample(n=min(args.sample, len(df)), random_state=42)

    client = OpenAI(api_key=api_key)

    print('Classificando', len(sample), 'exemplos com GPT-4.1-nano (padrão temperatura=0)...')
    preds, confs, justs = classify_with_gpt(client, sample['text'].tolist(), batch_size=1, pause_s=0.8)

    sample = sample.reset_index(drop=True)
    sample['pred'] = preds
    sample['confidence'] = confs
    sample['justification'] = justs

    # Evaluate
    true = sample['label_norm'].tolist()
    pred = sample['pred'].tolist()

    print('\nResultados:')
    print('Accuracy:', accuracy_score(true, pred))
    print('\nRelatório completo:')
    print(classification_report(true, pred))

    # Save
    os.makedirs('results', exist_ok=True)
    sample.to_csv('results/evaluation_results.csv', index=False)
    print('\nAmostra com previsões salva em results/evaluation_results.csv')


if __name__ == '__main__':
    main()
