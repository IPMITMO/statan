using SQLite;

namespace Statan.Database.Entities
{
    public class BaseEntity
    {
        [Column("id")]
        public int Id { get; set; }
    }
}
