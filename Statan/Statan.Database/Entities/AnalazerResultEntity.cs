using SQLite;

namespace Statan.Database.Entities
{
    [Table("AnalyzerResult")]
    public class AnalazerResultEntity : BaseEntity
    {
        [Column("origin")]
        public string Origin { get; set; }

        [Column("language")]
        public string Language { get; set; }

        [Column("language_ver")]
        public string LanguageVersion { get; set; }

        [Column("project_name")]
        public string ProjectName { get; set; }

        [Column("project_version")]
        public string ProjectVersion { get; set; }

        [Column("source_file_path")]
        public string SourceFilePath { get; set; }

        [Column("message")]
        public string Message { get; set; }

        [Column("start_line")]
        public int StartLine { get; set; }

        [Column("severity")]
        public int Severity { get; set; }

        [Column("diffs")]
        public string Diffs { get; set; }

        [Column("confidence")]
        public int Confidence { get; set; }

        [Column("params")]
        public string Params { get; set; }
    }
}
