using System;
using Statan.Core.Repository;
using System.Collections.Generic;
using System.Data;
using System.Web.Mvc;
using System.Linq;
using Statan.Web.Models;

namespace Statan.Web.Controllers
{
    public class HomeController : Controller
    {
        private readonly IAnalyzerResultRepository analyzerResultRepository;

        private static Dictionary<string, List<string>> projectVersions;

        public HomeController(IAnalyzerResultRepository analyzerResultRepository)
        {
            this.analyzerResultRepository = analyzerResultRepository;
        }

        public ActionResult Index()
        {
            return View();
        }

        [HttpGet]
        public ActionResult ProjectVersionResults()
        {
            var results = this.analyzerResultRepository.GetAll().ToList();

            var projects = results.GroupBy(x => x.ProjectName);
            projectVersions = projects
                .ToDictionary(k => k.Key, v => v.Select(x => x.ProjectVersion).Distinct().ToList());

            var projectVersionsModel = new ProjectVersionViewModel
            {
                Projects = projects.Select(x => new SelectListItem { Value = x.Key, Text = x.Key })
            };

            return View(projectVersionsModel);
        }

        public ActionResult GetProjectVersions(string projectName)
        {
            var versions = projectVersions[projectName]
                .Select(x => new SelectListItem { Text = x, Value = x});

            return Json(versions, JsonRequestBehavior.AllowGet);
        }


        [HttpGet]
        public ActionResult Results()
        {
            var results = this.analyzerResultRepository.GetAll();
            return View(results);
        }

        [HttpPost]
        [Route("Home/NewChart")]
        public JsonResult NewChart(string project, string version)
        {
            var results = this.analyzerResultRepository.GetAll()
                .Where(x => string.Equals(x.ProjectName, project, StringComparison.InvariantCultureIgnoreCase) 
                    && x.ProjectVersion == version);

            //Creating data  
            DataTable dt = new DataTable();
            dt.Columns.Add("Analyzer", Type.GetType("System.String"));
            dt.Columns.Add("Messages", Type.GetType("System.Int32"));

            var test = results.GroupBy(x => x.Origin).ToList();

            foreach (var g in results.GroupBy(x => x.Origin))
            {
                DataRow dr = dt.NewRow();
                dr["Analyzer"] = g.Key;
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