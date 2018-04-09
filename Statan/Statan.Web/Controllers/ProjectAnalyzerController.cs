using Statan.Core.Repository;
using Statan.Web.Models;
using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Web.Mvc;

namespace Statan.Web.Controllers
{
    public class ProjectAnalyzerController : Controller
    {
        private readonly IAnalyzerResultRepository analyzerResultRepository;

        private static Dictionary<string, List<string>> projectAnalyzers;

        public ProjectAnalyzerController(IAnalyzerResultRepository analyzerResultRepository)
        {
            this.analyzerResultRepository = analyzerResultRepository;
        }

        [HttpGet]
        public ActionResult Results()
        {
            var results = this.analyzerResultRepository.GetAll().ToList();

            var projects = results.GroupBy(x => x.ProjectName);
            projectAnalyzers = projects
                .ToDictionary(k => k.Key, v => v.Select(x => x.Origin).Distinct().ToList());

            var projectAnalyzersModel = new ProjectAnalyzerViewModel
            {
                Projects = projects.Select(x => new SelectListItem { Value = x.Key, Text = x.Key })
            };

            return View(projectAnalyzersModel);
        }

        public ActionResult GetProjectAnalyzers(string projectName)
        {
            var analyzers = projectAnalyzers[projectName]
                .Select(x => new SelectListItem { Text = x, Value = x });

            return Json(analyzers, JsonRequestBehavior.AllowGet);
        }

        [HttpPost]
        public JsonResult NewChart(string project, string analyzer)
        {
            var results = this.analyzerResultRepository.GetAll()
                .Where(x => string.Equals(x.ProjectName, project, StringComparison.InvariantCultureIgnoreCase)
                    && x.Origin == analyzer);

            //Creating data  
            DataTable dt = new DataTable();
            dt.Columns.Add("Version", Type.GetType("System.String"));
            dt.Columns.Add("Messages", Type.GetType("System.Int32"));

            foreach (var g in results.GroupBy(x => x.ProjectVersion))
            {
                DataRow dr = dt.NewRow();
                dr["Version"] = g.Key;
                dr["Messages"] = g.Count();
                dt.Rows.Add(dr);
            }

            //Looping and extracting each DataColumn to List<Object>  
            List<object> iData = new List<object>();
            foreach (DataColumn dc in dt.Columns)
            {
                List<object> x = new List<object>();
                x = (from DataRow drr in dt.Rows select drr[dc.ColumnName]).ToList();
                iData.Add(x);
            }
            //Source data returned as JSON  
            return Json(iData, JsonRequestBehavior.AllowGet);
        }
    }
}