using System.Collections.Generic;
using System.Web.Mvc;

namespace Statan.Web.Models
{
    public class ProjectVersionViewModel
    {
        public string Project { get; set; }

        public IEnumerable<SelectListItem> Projects { get; set; }

        public IEnumerable<SelectListItem> Versions { get; set; }

        public string Version { get; set; }
    }
}