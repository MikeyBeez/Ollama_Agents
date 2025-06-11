#!/usr/bin/env python3

import asyncio
from src.tests.test_memory_integration import run_all_tests

if __name__ == "__main__":
    asyncio.run(run_all_tests())