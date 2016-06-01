## QuickClassify

QuickClassify is a very basic text classification library based on Bayesian Algorithm.
Using Redis for persist learning data probs.

## Usage

### Train Data :

```
from QuickClassify import Classifier
classifier = Classifier()
classifier.train("Hazelcast is the best product for in-memory grid","inmemory_tools")

```
### Classification :

```
from QuickClassify import Classifier
classifier = Classifier()
classifier.classify("Apache Kafka is publish-subscribe messaging rethought as a distributed commit log.")
```