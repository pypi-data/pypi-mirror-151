from databases import Database
from .context import Context
from box import Box

def store_handler(ctx: Context, **kwargs):
    """ a store handler will configure stores onto context """
    
    if kwargs.get('type', None) == 'mariadb':
        store = kwargs.get('store')
        config = kwargs.get('config')
        username = config.get('username')
        password = config.get('password')
        host = config.get('host')
        port = config.get('port')
        database = config.get('database')
        conn = f"mysql://{username}:{password}@{host}:{port}/{database}"
        db = Database(conn)

        async def fetch_one(query: str, values:dict = {}):
            await db.connect()
            results = await db.fetch_one(query=query, values=values)
            await db.disconnect()
            return results
        
        async def fetch_all(query: str, values:dict = {}):
            await db.connect()
            results = await db.fetch_all(query=query, values=values)
            await db.disconnect()
            return results
        
        async def execute(query: str, values:dict = {}):
            await db.connect()
            results = await db.execute(query=query, values=values)
            await db.disconnect()
            return results
        
        async def execute_many(query: str, values:dict = {}):
            await db.connect()
            results = await db.execute_many(query=query, values=values)
            await db.disconnect()
            return results
        
        async def iterate(query: str, values:dict = {}):
            await db.connect()
            yield await db.iterate(query=query, values=values)
            await db.disconnect()
        
        ctx.stores[store] = Box({})
        ctx.stores[store].fetch_one = fetch_one
        ctx.stores[store].fetch_all = fetch_all
        ctx.stores[store].execute = execute
        ctx.stores[store].execute_many = execute_many
        ctx.stores[store].iterate = iterate
