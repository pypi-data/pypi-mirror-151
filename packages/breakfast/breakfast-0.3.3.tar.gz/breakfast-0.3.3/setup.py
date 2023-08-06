# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['breakfast']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'networkx>=2.8,<3.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'scipy>=1.8.0,<2.0.0']

entry_points = \
{'console_scripts': ['breakfast = breakfast.console:main']}

setup_kwargs = {
    'name': 'breakfast',
    'version': '0.3.3',
    'description': 'breakfast: fast putative outbreak cluster and infection chain detection using SNPs',
    'long_description': '# breakfast - FAST outBREAK detection and sequence clustering\n\n[![Tests](https://github.com/rki-mf1/breakfast/workflows/Tests/badge.svg)](https://github.com/rki-mf1/breakfast/actions?workflow=Tests)\n\n`breakfast` is a simple and fast script developed for clustering SARS-CoV-2 genomes using precalculated sequence features (e.g. nucleotide substitutions) from [covSonar](https://gitlab.com/s.fuchs/covsonar) or [Nextclade](https://clades.nextstrain.org/).\n\n**This project is under development and in experimental stage**\n\n<img src="/img/breakfast_logo_2.png" width="300">\n\n## Installation\n\n### Installation using pip\n\n```\n$ pip install breakfast\n```\n\n### System Dependencies\n\n`breakfast` runs under Python 3.10 and later. The base requirements are networkx, pandas, numpy, scikit-learn, click, and scipy.\n\n### Install using conda\n\nWe recommend using conda for installing all necessary dependencies:\n\n```\nconda env create -n sonar -f covsonar/sonar.env.yml\nconda env create -n breakfast -f breakfast/envs/sc2-breakfast.yml\n```\n\n## Example Command Line Usage\n\n### Simple test run\n```\nconda activate breakfast\nbreakfast/src/breakfast.py \\\n   --input-file breakfast/test/testfile.tsv  \\\n   --max-dist 1 \\\n   --outdir test-run/\n```\nYou will find your results in `test-run/cluster.tsv`, which should be identical to `breakfast/test/expected_clusters_dist1.tsv`\n\n\n### 1) covSonar + breakfast\nSequence processing with [covSonar](https://gitlab.com/s.fuchs/covsonar)\n```\nconda activate sonar\ncovsonar/sonar.py add -f genomes.fasta --db mydb --cpus 8\ncovsonar/sonar.py match --tsv --db mydb > genomic_profiles.tsv\n```\n\nClustering with a maximum SNP-distance of 1 and excluding clusters below a size of 5 sequences\n```\nconda activate breakfast\nbreakfast/src/breakfast.py \\\n   --input-file genomic_profiles.tsv \\\n   --max-dist 1 \\\n   --min-cluster-size 5 \\\n   --outdir covsonar-breakfast-results/\n```\n\n### 2) Nextclade + breakfast\n\nSequence processing with [Nextclade CLI](https://clades.nextstrain.org/).\n\n```\nconda install -c bioconda nextclade\nnextclade dataset get --name \'sars-cov-2\' --output-dir \'data/sars-cov-2\'\nnextclade \\\n   --in-order \\\n   --input-fasta genomes.fasta \\\n   --input-dataset data/sars-cov-2 \\\n   --output-tsv output/nextclade.tsv \\\n   --output-tree output/nextclade.auspice.json \\\n   --output-dir output/ \\\n   --output-basename nextclade\n```\n\nAlternatively, you can also use [Nextclade Web](https://clades.nextstrain.org/) to process your fasta and export the genomic profile as "nextclade.tsv".\n\nClustering with a maximum SNP-distance of 1 and excluding clusters below a size of 5 sequences. Since the input tsv of Nextclade looks a little different from the covSonar tsv, you need to specify the additional parameters `--id-col`, `--clust-col` and `--sep2` for identifying the correct columns.\n\n```\nconda activate breakfast\nbreakfast/src/breakfast.py \\\n   --input-file output/nextclade.tsv \\\n   --max-dist 1 \\\n   --min-cluster-size 5 \\\n   --id-col "seqName" \\\n   --clust-col "substitutions" \\\n   --sep2 "," \\\n   --outdir nextclade-breakfast-results/\n```\n\n## Parameter description\n\n| Parameter              | Type    \t| Required | Default \t| Description                                |\n|----------------------- |---------\t|----------|----------|------------------------------------------  |\n| --input-file           | String     \t|✅\t     | \'genomic_profiles.tsv.gz\'    \t| Path of the input file (in tsv format)     |\n| --max-dist              | Integer  \t|\t     | 1     \t| Two sequences will be grouped together, if their pairwise edit distance does not exceed this threshold |\n| --min-cluster-size  | Integer  \t|      | 2     \t| Minimum number of sequences a cluster needs to include to be defined in the result file      |\n| --id-col    | String \t|     | \'accession\'      \t| Name of the sequence identifier column of the input file          |\n| --clust-col              | String \t|     | \'dna_profile\'      | Name of the mutation profile column of the input file         |\n| --var-type              | String \t|     | \'dna\'       | Specify if DNA or AA substitutions are used for the mutation profiles         |\n| --sep              | String \t|     | \'\\t\'      | Input file separator       |\n|  --sep2              | String \t|     | \'  \'      | Secondary clustering column separator (between each mutation)        |\n| --outdir              | String \t|     | \'output/\'       | Path of output directory        |\n| --trim-start               | Integer \t|     |264       | Bases to trim from the beginning         |\n| --trim-end               | Integer \t|     | 228       | Bases to trim from the end         |\n| --reference-length              | Integer \t|     | 29903      | Length of reference genome (defaults to NC_045512.2)        |\n| --skip-del               | Bool \t|     | TRUE       | Deletions will be skipped for calculating the pairwise distance of your input sequences.|\n| --skip-ins               | Bool \t|     | TRUE       | Insertions will be skipped for calculating the pairwise distance of your input sequences.         |\n| --input-cache           | Integer \t|     | None   | Path to import results from previous run |\n| --output-cache              | String \t|     | None       | Path to export results which can be used in the next run to decrease runtime.  |\n| --help                   | N/A     \t|\t   | N/A     \t| Show this help message and exit            |\n| --version                | N/A     \t|\t   | N/A     \t| Show version and exit            |\n',
    'author': 'Matthew Huska',
    'author_email': 'HuskaM@rki.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rki-mf1/breakfast',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
