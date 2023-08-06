"""Manage MediaItems of type Radio."""
from __future__ import annotations

from time import time

from music_assistant.helpers.database import TABLE_RADIOS
from music_assistant.helpers.json import json_serializer
from music_assistant.models.enums import EventType, MediaType
from music_assistant.models.event import MassEvent
from music_assistant.models.media_controller import MediaControllerBase
from music_assistant.models.media_items import Radio


class RadioController(MediaControllerBase[Radio]):
    """Controller managing MediaItems of type Radio."""

    db_table = TABLE_RADIOS
    media_type = MediaType.RADIO
    item_cls = Radio

    async def get_radio_by_name(self, name: str) -> Radio | None:
        """Get in-library radio by name."""
        return await self.mass.database.get_row(self.db_table, {"name": name})

    async def add(self, item: Radio) -> Radio:
        """Add radio to local db and return the new database item."""
        item.metadata.last_refresh = int(time())
        await self.mass.metadata.get_radio_metadata(item)
        db_item = await self.add_db_item(item)
        self.mass.signal_event(
            MassEvent(EventType.RADIO_ADDED, object_id=db_item.uri, data=db_item)
        )
        return db_item

    async def add_db_item(self, radio: Radio) -> Radio:
        """Add a new radio record to the database."""
        assert radio.provider_ids
        async with self.mass.database.get_db() as _db:
            match = {"name": radio.name}
            if cur_item := await self.mass.database.get_row(
                self.db_table, match, db=_db
            ):
                # update existing
                return await self.update_db_item(cur_item["item_id"], radio)

            # insert new radio
            new_item = await self.mass.database.insert_or_replace(
                self.db_table, radio.to_db_row(), db=_db
            )
            item_id = new_item["item_id"]
            # store provider mappings
            await self.mass.music.set_provider_mappings(
                item_id, MediaType.RADIO, radio.provider_ids, db=_db
            )
            self.logger.debug("added %s to database", radio.name)
            # return created object
            return await self.get_db_item(item_id, db=_db)

    async def update_db_item(
        self, item_id: int, radio: Radio, overwrite: bool = False
    ) -> Radio:
        """Update Radio record in the database."""
        async with self.mass.database.get_db() as _db:
            cur_item = await self.get_db_item(item_id, db=_db)
            if overwrite:
                metadata = radio.metadata
                provider_ids = radio.provider_ids
            else:
                metadata = cur_item.metadata.update(radio.metadata)
                provider_ids = {*cur_item.provider_ids, *radio.provider_ids}

            match = {"item_id": item_id}
            await self.mass.database.update(
                self.db_table,
                match,
                {
                    "name": radio.name,
                    "sort_name": radio.sort_name,
                    "metadata": json_serializer(metadata),
                    "provider_ids": json_serializer(provider_ids),
                },
                db=_db,
            )
            await self.mass.music.set_provider_mappings(
                item_id, MediaType.RADIO, provider_ids, db=_db
            )
            self.logger.debug("updated %s in database: %s", radio.name, item_id)
            return await self.get_db_item(item_id, db=_db)
