import aiomysql, logging

__pool = None

async def create_pool(loop, **kw):
    logging.info('create database connection pool ...')
    global __pool
    __pool = await aiomysql.create_pool(loop=loop, **kw)


async def execute(sql, args = None):
    logging.info(sql)
    global __pool
    with await __pool as conn:
        try:
            cur = await conn.cursor(aiomysql.DictCursor)
            await cur.execute(sql.replace('?', '%s'), args or ())
            rs = await cur.fetchall()
            affected = cur.rowcount
            await cur.close()
        except BaseException as e:
            raise
        return rs, affected

