""" Read pv functions """
import logging
from datetime import datetime
from typing import List, Optional, Union

from sqlalchemy import desc
from sqlalchemy.orm import Session

from nowcasting_datamodel.models import PVSystemSQL, PVYieldSQL

logger = logging.getLogger(__name__)


def get_pv_systems(
    session: Session,
    pv_systems_ids: Optional[List[int]] = None,
    provider: Optional[str] = "pvoutput.org",
) -> List[PVSystemSQL]:
    """
    Get all pv systems

    :param session:
    :param pv_systems_ids: optional list of ids
    :param provider: optional provider name
    :return: list of pv systems
    """

    # start main query
    query = session.query(PVSystemSQL)
    query = query.distinct(PVSystemSQL.id)

    # filter on pv_system_id and provider
    if pv_systems_ids is not None:
        query = query.filter(PVSystemSQL.pv_system_id.in_(pv_systems_ids))
        query = query.filter(PVSystemSQL.provider == provider)

    # order by 'created_utc' desc, so we get the latest one
    query = query.order_by(PVSystemSQL.id, desc(PVSystemSQL.created_utc))

    # get all results
    pv_systems = query.all()

    return pv_systems


def get_latest_pv_yield(
    session: Session,
    pv_systems: List[PVSystemSQL],
    append_to_pv_systems: bool = False,
    start_datetime_utc: Optional[datetime] = None,
    start_created_utc: Optional[datetime] = None,
) -> Union[List[PVYieldSQL], List[PVSystemSQL]]:
    """
    Get the last pv yield data

    :param session: database sessions
    :param pv_systems: list of pv systems
    :param append_to_pv_systems: append pv yield to pv systems, or return pv systems.
        If appended the yield is access by 'pv_system.last_pv_yield'
    :param start_created_utc: search filters > on 'created_utc'. Can be None
    :param start_datetime_utc: search filters > on 'datetime_utc'. Can be None
    :return: either list of pv yields, or pv systems
    """

    logger.info("Getting latest pv yield")

    pv_systems_ids = [pv_system.id for pv_system in pv_systems]

    # start main query
    query = session.query(PVYieldSQL)
    query = query.join(PVSystemSQL)
    query = query.where(
        PVSystemSQL.id == PVYieldSQL.pv_system_id,
    )

    # only select on results per pv system
    query = query.distinct(PVSystemSQL.id)

    # select only th epv systems we want
    query = query.where(PVSystemSQL.id.in_(pv_systems_ids))

    # filter on datetime utc
    if start_datetime_utc is not None:
        query = query.filter(PVYieldSQL.datetime_utc >= start_datetime_utc)

    # filter on created utc
    if start_created_utc is not None:
        query = query.filter(PVYieldSQL.created_utc >= start_created_utc)

    # order by 'created_utc' desc, so we get the latest one
    query = query.order_by(
        PVSystemSQL.id, desc(PVYieldSQL.datetime_utc), desc(PVYieldSQL.created_utc)
    )

    # get all results
    pv_yields: List[PVYieldSQL] = query.all()

    if not append_to_pv_systems:
        return pv_yields
    else:
        logger.info("Will be returning pv systems")

        # get list of pvsystems with last pv yields
        pv_systems_with_pv_yields = []
        for pv_yield in pv_yields:
            pv_system = pv_yield.pv_system
            pv_system.last_pv_yield = pv_yield

            pv_systems_with_pv_yields.append(pv_system)

        # add pv systems that dont have any pv yields
        pv_systems_with_pv_yields_ids = [pv_system.id for pv_system in pv_systems_with_pv_yields]

        logger.debug(f"Found {len(pv_systems_with_pv_yields_ids)} pv systems with pv yields")

        pv_systems_with_no_pv_yields = []
        for pv_system in pv_systems:
            if pv_system.id not in pv_systems_with_pv_yields_ids:
                pv_system.last_pv_yield = None

                pv_systems_with_no_pv_yields.append(pv_system)

        logger.debug(f"Found {len(pv_systems_with_no_pv_yields)} pv systems with no pv yields")

        all_pv_systems = pv_systems_with_pv_yields + pv_systems_with_no_pv_yields

        return all_pv_systems


def get_pv_yield(
    session: Session,
    pv_systems_ids: Optional[List[int]] = None,
    start_utc: Optional[datetime] = None,
    end_utc: Optional[datetime] = None,
) -> Union[List[PVYieldSQL], List[PVSystemSQL]]:
    """
    Get the last pv yield data

    :param session: database sessions
    :param pv_systems_ids: list of pv systems ids
    :return: either list of pv yields, or pv systems
    """

    # start main query
    query = session.query(PVYieldSQL)
    query = query.join(PVSystemSQL)

    # select only th pv systems we want
    if pv_systems_ids is not None:
        query = query.where(PVSystemSQL.pv_system_id.in_(pv_systems_ids))

    # filter on start time
    if start_utc is not None:
        query = query.filter(PVYieldSQL.datetime_utc >= start_utc)

    # filter on end time
    if end_utc is not None:
        query = query.filter(PVYieldSQL.datetime_utc < end_utc)

    # order by 'created_utc' desc, so we get the latest one
    query = query.order_by(
        PVSystemSQL.id,
        PVYieldSQL.datetime_utc,
    )

    # get all results
    pv_yields: List[PVYieldSQL] = query.all()

    return pv_yields
