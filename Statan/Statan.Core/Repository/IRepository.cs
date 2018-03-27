using System.Collections.Generic;

namespace Statan.Core.Repository
{
    public interface IRepository<T> where T : class, new()
    {
        List<T> Get();
        T Get(int id);
        int Insert(T entity);
        void Update(T entity);
        void Delete(T entity);
    }
}
