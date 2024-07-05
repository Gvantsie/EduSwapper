# Description: This file contains country choices for user model.
from model_utils import Choices
import pycountry

# Generate country choices using pycountry
COUNTRY_CHOICES = Choices(
    *[(country.alpha_2, country.name) for country in pycountry.countries]
)
