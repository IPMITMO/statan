using SQLite;
using Statan.Core.Repository;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web.Configuration;

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
            this.Db = new SQLiteConnection(WebConfigurationManager.AppSettings["DatabasePath"]);
        }

        public void Delete(T entity)
        {
            this.Db.Delete(entity);
        }

        public IEnumerable<T> Get()
        {
            return this.Db.Table<T>().AsEnumerable();
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
