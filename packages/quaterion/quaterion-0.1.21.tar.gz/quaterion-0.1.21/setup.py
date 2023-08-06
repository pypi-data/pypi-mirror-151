# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quaterion',
 'quaterion.dataset',
 'quaterion.distances',
 'quaterion.eval',
 'quaterion.eval.accumulators',
 'quaterion.eval.group',
 'quaterion.eval.pair',
 'quaterion.eval.samplers',
 'quaterion.loss',
 'quaterion.loss.extras',
 'quaterion.train',
 'quaterion.train.cache',
 'quaterion.utils']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0',
 'mmh3>=3.0.0,<4.0.0',
 'pytorch-lightning>=1.5.8,<2.0.0',
 'quaterion-models>=0.1.9',
 'torch>=1.8.2']

extras_require = \
{'full': ['pytorch-metric-learning>=1.3.0,<2.0.0'],
 'pytorch-metric-learning': ['pytorch-metric-learning>=1.3.0,<2.0.0']}

setup_kwargs = {
    'name': 'quaterion',
    'version': '0.1.21',
    'description': 'Metric Learning fine-tuning framework',
    'long_description': '# Quaterion\n\n>  A dwarf on a giant\'s shoulders sees farther of the two \n\nQuaterion is a framework for fine-tuning similarity learning models.\nThe framework closes the "last mile" problem in training models for semantic search, recommendations, anomaly detection, extreme classification, matching engines, e.t.c.\n\nIt is designed to combine the performance of pre-trained models with specialization for the custom task while avoiding slow and costly training.\n\n\n## Features\n\n* 🌀 **Warp-speed fast**: With the built-in caching mechanism, Quaterion enables you to train thousands of epochs with huge batch sizes even on *laptop GPU*.\n\n<!-- GIF HERE -->\n\n* 🐈\u200d **Small data compatible**: Pre-trained models with specially designed head layers allow you to benefit even from a dataset you can label *in one day*.\n\n\n* 🏗️ **Customizable**: Quaterion allows you to re-define any part of the framework, making it flexible even for large-scale and sophisticated training pipelines.\n\n## Installation\n\nTL;DR:\n\nFor training:\n```bash\npip install quaterion\n```\n\nFor inference service:\n```bash\npip install quaterion-models\n```\n\n---\n\nQuaterion framework consists of two packages - `quaterion` and [`quaterion-models`](https://github.com/qdrant/quaterion-models).\n\nSince it is not always possible or convenient to represent a model in ONNX format (also, it **is supported**), the Quaterion keeps a very minimal collection of model classes, which might be required for model inference, in a [separate package](https://github.com/qdrant/quaterion-models).\n\nIt allows avoiding installing heavy training dependencies into inference infrastructure: `pip install quaterion-models`\n\nAt the same time, once you need to have a full arsenal of tools for training and debugging models, it is available in one package: `pip install quaterion`\n\n## Architecture\n\nQuaterion is built on top of [PyTorch Lightning](https://github.com/PyTorchLightning/pytorch-lightning) - a framework for high-performance AI research.\nIt takes care of all the tasks involved in constructing a training loops for ML models:\n\n- Epochs management -> [[tutorial](https://pytorch-lightning.readthedocs.io/en/latest/model/train_model_basic.html)]\n- Logging -> [[tutorial](https://pytorch-lightning.readthedocs.io/en/latest/extensions/logging.html?highlight=logging)]\n- Early Stopping -> [[tutorial](https://pytorch-lightning.readthedocs.io/en/latest/common/early_stopping.html)]\n- Checkpointing -> [[tutorial](https://pytorch-lightning.readthedocs.io/en/latest/common/checkpointing.html)]\n- Distributed training -> [[tutorial](https://pytorch-lightning.readthedocs.io/en/latest/clouds/cluster.html)]\n- [And many more](https://pytorch-lightning.readthedocs.io/en/latest/starter/introduction.html)\n\nIn addition to PyTorch Lightning functionality, Quaterion provides a scaffold for defining:\n\n- Fine-tunable similarity learning models\n  - Encoders and Head Layers\n- Datasets and Data Loaders for representing similarity information\n- Loss functions for similarity learning\n- Metrics for evaluating model performance\n\n<!--\n\n<details>\n    <summary>Imports and definitions</summary>\n    \n```python\nimport torch\nfrom torch import nn\nimport torchvision\nfrom quaterion import TrainableModel\nfrom quaterion.loss import SimilarityLoss, TripletLoss\n\nfrom quaterion_models.encoders import Encoder\nfrom quaterion_models.heads import EncoderHead, SkipConnectionHead\n\nclass MobilenetV3Encoder(Encoder):\n    """Example of an Encoder for images, initialized from the pre-trained model\n    """\n    def __init__(self, embedding_size: int):\n        super().__init__()\n        # Download and initialize pre-trained model\n        self.encoder = torchvision.models.mobilenet_v3_small(pretrained=True)\n        # We remove last layer of the model, so that it will return raw embeddings\n        self.encoder.classifier = nn.Identity()\n\n        self._embedding_size = embedding_size\n\n    @property\n    def trainable(self) -> bool:\n        return False  # We will only tune the head layer\n\n    @property\n    def embedding_size(self) -> int:\n        return self._embedding_size  # Output size of this encoder\n\n    def forward(self, images):\n        return self.encoder.forward(images)\n\n```\n</details>\n\n```python\n\nclass Model(TrainableModel):\n    def __init__(self, embedding_size: int, lr: float):\n        self._embedding_size = embedding_size\n        self._lr = lr\n        super().__init__()\n\n    def configure_encoders(self) -> Encoder:\n        # Define one or multiple encoders for the input data.\n        # Each encoder could represent its own part of the data, \n        # or different aspects of the same object.\n        return MobilenetV3Encoder(self._embedding_size)\n\n    def configure_head(self, input_embedding_size) -> EncoderHead:\n        # Forward concatenated encoder output into final trainable layer\n        return SkipConnectionHead(input_embedding_size)\n\n    def configure_loss(self) -> SimilarityLoss:\n        # Define which loss function to use during the fine-tuning.\n        return TripletLoss()\n\n    def configure_optimizers(self):\n        # And also which optimizer to use\n        return torch.optim.Adam(self.model.parameters(), self._lr)\n```\n\n-->\n',
    'author': 'generall',
    'author_email': 'andrey@vasnetsov.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/qdrant/quaterion',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
