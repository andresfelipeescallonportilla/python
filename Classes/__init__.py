"""Paquete ``Classes`` (equivalente al paquete Java ``Classes``).

Contiene las entidades de dominio:
    - ``cls_pet.clsPet``            (clase base)
    - ``cls_dog.clsDog``
    - ``cls_cat.clsCat``
    - ``cls_doctor.clsDoctor``
    - ``cls_veterinary.clsVeterinary``
    - ``abst_hospital.AbstHospital``
    - ``cls_report_by_health_status.clsReportByHealthStatus``
"""

from .abst_hospital import AbstHospital
from .cls_cat import clsCat
from .cls_doctor import clsDoctor
from .cls_dog import clsDog
from .cls_pet import clsPet
from .cls_report_by_health_status import clsReportByHealthStatus
from .cls_veterinary import clsVeterinary

__all__ = [
    "AbstHospital",
    "clsCat",
    "clsDoctor",
    "clsDog",
    "clsPet",
    "clsReportByHealthStatus",
    "clsVeterinary",
]
