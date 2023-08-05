import rocksdb
from rocksdb.errors import RocksIOError
from os import makedirs, remove
from nubium_utils.confluent_utils.confluent_runtime_vars import env_vars


class RdbTableInUse(Exception):
    def __init__(self, table_name):
        super().__init__(f'Table "{table_name}" is currently in use by another instance.')


class RDB:
    def __init__(self, table_name, table_path=None, delete_current_lock=False):
        self.rdb = None
        self.table_name = table_name
        self._delete_current_lock = delete_current_lock

        if not table_path:
            table_path = env_vars()['NU_TABLE_PATH']
        makedirs(table_path, exist_ok=True)
        self.full_db_path = f"{table_path}/{table_name}.rocksdb"

        self._init_rdb()

    def _init_rdb(self):
        opts = rocksdb.Options()
        opts.create_if_missing = True
        opts.max_open_files = 10000
        opts.write_buffer_size = self.get_mb(32)
        opts.max_write_buffer_number = 2
        opts.target_file_size_base = self.get_mb(32)

        opts.table_factory = rocksdb.BlockBasedTableFactory(
            filter_policy=rocksdb.BloomFilterPolicy(10),
            block_cache=rocksdb.LRUCache(2 * (1024 ** 3)),
            block_cache_compressed=rocksdb.LRUCache(500 * (1024 ** 2)))
        try:
            self.rdb = rocksdb.DB(self.full_db_path, opts)
        except RocksIOError as e:
            if 'Resource temporarily unavailable' or 'No locks available' in e.args[0].decode():
                if self._delete_current_lock:
                    self.delete_lock_file()
                    self._delete_current_lock = False
                    self._init_rdb()
                else:
                    raise RdbTableInUse(self.table_name)
            else:
                raise

    def get_mb(self, value):
        return value * 2**20

    def write(self, key, value):
        self.rdb.put(key.encode(), value.encode())

    def write_batch(self, write_dict):
        batch = rocksdb.WriteBatch()
        for k, v in write_dict.items():
            try:
                v = v.encode()
            except ValueError:
                pass
            batch.put(k.encode(), v)
        self.rdb.write(batch)

    def read(self, k):
        result = self.rdb.get(k.encode())
        if result:
            return result.decode()
        return result

    def delete(self, key):
        self.rdb.delete(key.encode())

    def delete_lock_file(self):
        remove(f'{self.full_db_path}/LOCK')

    def close(self):
        # TODO: Add flush method
        self.rdb.close()
