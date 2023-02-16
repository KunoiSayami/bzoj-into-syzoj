#!/usr/bin/env python
from __future__ import annotations
import asyncio
import dataclasses
import json
import os

import aiofiles
import aiohttp


URL = 'http://127.0.0.1:8080/problem/'


@dataclasses.dataclass
class SYZOJData:

    id: int
    title: str
    description: str
    input_format: str
    output_format: str
    example: str
    limit_and_hint: str

    @staticmethod
    def parse_images(src: str) -> str:
        if '://' not in src:
            return f"/subscribe-to-technoblade/image/{src}"
        return src

    @classmethod
    def parse_description(cls, problem: dict) -> str:
        if len(img := problem['img']):
            group = '\n<br />'.join(map(lambda x: f'<img src="{cls.parse_images(x)}">', img))
            return f"{problem['description']}\n<br />{group}"
        return problem['description']

    @classmethod
    def from_json(cls, problem: dict) -> SYZOJData:
        return cls(problem['id'], problem['title'], cls.parse_description(problem),
                   problem['input_format'], problem['output_format'],
                   f"Sample input:\n<br />{problem['input_sample']}<br />"
                   f"<br />Sample output:\n<br />{problem['output_sample']}",
                   f"{problem['hint']}\n<br />\n<br />Source: {problem['source']}")


async def send_problem(problem: dict, session: aiohttp.ClientSession):
    async with session.post(f'{URL}{problem["id"]}/edit', data=SYZOJData.from_json(problem).__dict__) as _response:
        pass
    async with session.post(f'{URL}{problem["id"]}/public') as _response:
        pass


async def main():
    client = aiohttp.ClientSession(
        cookies=(('login', '%5B%22root%22%2C%%22%5D'),)
    )
    tasks = []
    for item in os.listdir('bzojch-master/json'):
        async with aiofiles.open(f'bzojch-master/json/{item}') as fin:
            problem = json.loads(await fin.read())
            try:
                tasks.append(asyncio.create_task(send_problem(problem, client)))
            except InterruptedError:
                break
    try:
        while True:
            done, pending = await asyncio.wait(tasks, timeout=1, return_when=asyncio.ALL_COMPLETED)
            print(f"\r{len(done): 4}", len(pending), end='')
            if not len(pending):
                break
    except KeyboardInterrupt:
        pass
    await client.close()


if __name__ == '__main__':
    asyncio.run(main())

