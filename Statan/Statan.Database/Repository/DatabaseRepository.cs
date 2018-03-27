using SQLite;
using Statan.Core.Repository;
using System.Collections.Generic;
using System.Linq;

namespace Statan.Database.Repository
{
    internal class DatabaseRepository<T> : IRepository<T>
        where T : class, new()
    {
        private SQLiteConnection Db { get; set; }

        protected TableQuery<T> Collection
        {
            get
            {
                return this.Db.Table<T>();
            }
        }

        public DatabaseRepository()
        {
            this.Db = new SQLiteConnection(@"../../../database2.sqlite");
        }

        public void Delete(T entity)
        {
            this.Db.Delete(entity);
        }

        public List<T> Get()
        {
            return this.Db.Table<T>().ToList();
        }

        public T Get(int id)
        {
            return this.Db.Find<T>(id);
        }

        public int Insert(T entity)
        {
            return this.Db.Insert(entity);
        }

        public void Update(T entity)
        {
            this.Db.Update(entity);
        }
    }
}
