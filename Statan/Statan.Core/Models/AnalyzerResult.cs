namespace Statan.Core.Models
{
    public class AnalyzerResult
    {
        public int Id { get; set; }

        public string Origin { get; set; }

        public string Language { get; set; }

        public string LanguageVersion { get; set; }

        public string ProjectName { get; set; }

        public string ProjectVersion { get; set; }

        public string SourceFilePath { get; set; }

        public string Message { get; set; }

        public int StartLine { get; set; }

        public int Severity { get; set; }

        public string Diffs { get; set; }

        public int Confidence { get; set; }

        public string Params { get; set; }
    }
}
