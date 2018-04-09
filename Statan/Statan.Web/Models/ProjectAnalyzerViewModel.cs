using System.Collections.Generic;
using System.Web.Mvc;

namespace Statan.Web.Models
{
    public class ProjectAnalyzerViewModel
    {
        public string Project { get; set; }

        public IEnumerable<SelectListItem> Projects { get; set; }

        public IEnumerable<SelectListItem> Analyzers { get; set; }
        
        public string Analyzer { get; set; }
    }
}