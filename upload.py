import datetime
import asyncio
import aiohttp
from model import SwapiPeople, Session, engine, Base


class Swapi:
    base_url = 'https://swapi.dev/api/people/'

    def __init__(self, client):
        self.client = client
        self.next_page = self.base_url
        self.chunk = []

    async def __anext__(self):
        if self.next_page is None:
            raise StopAsyncIteration
        elif not self.chunk:
            async with self.client.get(self.next_page) as result:
                json_data = await result.json()
                self.next_page = json_data['next']
                self.chunk = json_data['results']
                result = self.chunk
                self.chunk = []
        return result

    def __aiter__(self):
        return self


async def paste_to_db(people_jsons):
    async with Session() as session:
        orm_objects = [SwapiPeople(
            name=item['name'],
            birth_year=item['birth_year'],
            eye_color=item['eye_color'],
            gender=item['gender'],
            hair_color=item['hair_color'],
            height=item['height'],
            mass=item['mass'],
            skin_color=item['skin_color'],
            homeworld=item['homeworld'],
            films=item['films'],
            species=item['species'],
            starships=item['starships'],
            vehicles=item['vehicles']
        ) for item in people_jsons]
        session.add_all(orm_objects)
        await session.commit()


async def main():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

    tasks = []
    async with aiohttp.ClientSession() as client:
        swapi_iter = Swapi(client)
        async for _ in swapi_iter:
            paste_to_db_coro = paste_to_db(_)
            paste_to_db_task = asyncio.create_task(paste_to_db_coro)
            tasks.append(paste_to_db_task)

    tasks = asyncio.all_tasks() - {asyncio.current_task(), }
    for task in tasks:
        await task

if __name__ == '__main__':
    start = datetime.datetime.now()
    asyncio.run(main())
    print(datetime.datetime.now() - start)
