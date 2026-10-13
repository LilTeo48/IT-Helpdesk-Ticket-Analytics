import random
from datetime import timedelta
from pathlib import Path

import pandas as pd
from faker import Faker

# Initialize our fake data generator
fake = Faker()

#Set random seeds for reproducible data
random.seed(42)
Faker.seed(42)