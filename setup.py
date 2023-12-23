import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TorToiSe",
    packages=setuptools.find_packages(),
    version="2.4.5",
    author="James Betker",
    author_email="james@adamant.ai",
    description="A high quality multi-voice text-to-speech library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.ecker.tech/mrq/tortoise-tts",
    project_urls={},
    scripts=[
        'scripts/tortoise_tts.py',
    ],
    include_package_data=True,
    install_requires=[
        'appdirs==1.4.4',
        'audio2numpy==0.1.2',
        'einops==0.7.0',
        'inflect==7.0.0',
        'librosa==0.8.1',
        'numba==0.58.1',
        'numpy==1.23.5',
        'progressbar2==4.2.0',
        'progressbar==2.5',
        'scipy==1.11.4',
        'text-unidecode==1.3',
        'threadpoolctl==3.2.0',
        'tokenizers==0.12.1',
        'torchaudio',
        'torchlibrosa==0.1.0',
        'tqdm==4.66.1',
        'transformers==4.25.0',
        'x-transformers==1.0.4',
        'psutil==5.9.7',
        'rotary_embedding_torch==0.4.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
