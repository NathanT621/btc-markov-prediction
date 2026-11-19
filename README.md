
# Bitcoin Price Direction Prediction

A quantitative research project investigating whether historical Bitcoin price movements can be used to predict the direction of subsequent 15-minute price movements.

The project compares stochastic models and machine learning approaches, with the longer-term goal of evaluating their potential applications to binary prediction markets.

## Overview

The primary research question is:

**Can historical BTC price movements provide meaningful predictive information about the direction of the next 15-minute period?**

The initial experiment uses higher-order Markov chains to estimate conditional probabilities based on previous Up/Down movements. Future experiments will explore statistical learning and machine learning models to determine whether more complex approaches improve predictive performance.

## Dataset

Historical 15-minute BTC/USDT candlestick data is obtained from the [BTC/USDT 15-Minute Dataset on Kaggle](https://www.kaggle.com/datasets/felixvo/15m-btcusdt).

- **Observations:** 183,073 price records
- **Frequency:** 15-minute intervals
- **Target:** Direction of the next price movement
- **Preprocessing:** Consecutive closing prices are classified as Up (`U`) or Down (`D`). Unchanged prices are classified as Down.

For the initial experiment, observations were divided chronologically into 80% training and 20% testing.

## Methodology

Models are trained on historical observations and evaluated on later, unseen periods.

The initial experiment estimates the conditional probability of the next movement given the previous $n$ movements:

$$
P(X_{t+1} \mid X_t, X_{t-1}, \ldots, X_{t-n+1})
$$

where $X_t \in \{U,D\}$.

For each historical pattern, the transition probabilities are estimated from the frequency of subsequent Up and Down movements.

The model predicts whichever direction has the higher conditional probability.

Model predictions are evaluated against a constant-direction baseline using classification accuracy.

Future experiments will incorporate additional evaluation metrics, including probability calibration, log loss, and Brier score.

## Experiments

| Experiment | Model | Status |
|---|---|---|
| 01 | Higher-Order Markov Chains | Implemented |
| 02 | Logistic Regression | Planned |
| 03 | Tree-Based Models | Planned |
| 04 | Neural Networks | Planned |

Each experiment will have its own documentation describing its methodology, implementation, and findings.

## Preliminary Results

The first experiment evaluated Markov chains of orders 1 through 9.

| Model | Test Accuracy |
|---|---:|
| Constant-direction baseline | 50.02% |
| 1st-order Markov | 52.35% |
| 2nd-order Markov | 52.44% |
| 3rd-order Markov | 52.55% |
| 4th-order Markov | 52.63% |
| 5th-order Markov | 52.76% |
| 6th-order Markov | 52.81% |
| 7th-order Markov | 52.73% |
| 8th-order Markov | **52.83%** |
| 9th-order Markov | 52.49% |

Higher-order models generally achieved slightly higher directional accuracy, with the eighth-order model performing best among those evaluated.

The first-order model was also evaluated across 10 consecutive segments of the test data, achieving accuracy above 50% in 9 out of 10 segments.

These findings are preliminary. Because multiple models were compared using the same test period, additional validation is necessary to determine whether the observed improvements generalize.

## Limitations

The initial analysis has several limitations:

- Models use historical price direction without incorporating price magnitude, trading volume, or volatility.
- Classification accuracy alone does not establish whether predicted probabilities are well calibrated.
- Transition probabilities may vary across market conditions and time periods.
- Repeated model comparison on the same test set introduces model-selection bias.
- Directional accuracy does not establish profitability or a positive expected return.

## Future Work

Planned extensions include:

- Evaluating models using chronological validation and walk-forward testing.
- Analyzing the calibration and stability of predicted probabilities.
- Introducing logistic regression and tree-based models.
- Implementing neural networks using PyTorch.
- Investigating whether additional features, such as volatility and trading volume, improve predictions.
- Investigating historical prediction-market pricing and potential discrepancies between estimated probabilities and market prices.

## Installation and Usage

Setup instructions and reproducible experiment commands will be added as the repository is reorganized.
