using Statan.Core.Repository;
using Statan.Web.Models;
using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Web.Mvc;

namespace Statan.Web.Controllers
{
    public class ProjectVersionController : Controller
    {
        private readonly IAnalyzerResultRepository analyzerResultRepository;

        private static Dictionary<string, List<string>> projectVersions;

        public ProjectVersionController(IAnalyzerResultRepository analyzerResultRepository)
        {
            this.analyzerResultRepository = analyzerResultRepository;
        }

        [HttpGet]
        public ActionResult Results()
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
                .Select(x => new SelectListItem { Text = x, Value = x });

            return Json(versions, JsonRequestBehavior.AllowGet);
        }

        [HttpPost]
        public JsonResult NewChart(string project, string version)
        {
            var results = this.analyzerResultRepository.GetAll()
                .Where(x => string.Equals(x.ProjectName, project, StringComparison.InvariantCultureIgnoreCase)
                    && x.ProjectVersion == version);

            //Creating data  
            DataTable dt = new DataTable();
            dt.Columns.Add("Analyzer", Type.GetType("System.String"));
            dt.Columns.Add("Messages", Type.GetType("System.Int32"));
            
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

        [HttpPost]
        public JsonResult BanditChart(string project, string version)
        {
            var results = this.analyzerResultRepository.GetAll()
                .Where(x => string.Equals(x.ProjectName, project, StringComparison.InvariantCultureIgnoreCase)
                    && x.ProjectVersion == version
                    && x.Origin == "BanditBear");

            //Creating data  
            DataTable dt = new DataTable();
            dt.Columns.Add("Code", Type.GetType("System.String"));
            dt.Columns.Add("Messages", Type.GetType("System.Int32"));

            foreach (var g in results.GroupBy(x => x.Params))
            {
                DataRow dr = dt.NewRow();
                dr["Code"] = g.Key;
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