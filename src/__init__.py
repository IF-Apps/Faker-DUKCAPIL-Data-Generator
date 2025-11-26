# DUKCAPIL Data Generator
# Generate dummy Indonesian citizen data with DUKCAPIL format

__version__ = "1.1.0"

from .family_generator import FamilyGenerator
from .parallel_generator import ParallelFamilyGenerator, get_optimal_workers
from .wilayah_loader import WilayahLoader, get_loader
from .id_generator import IDGenerator
