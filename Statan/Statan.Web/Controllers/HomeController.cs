using Statan.Core.Repository;
using System.Collections.Generic;
using System.Data;
using System.Web.Mvc;
using System.Linq;

namespace Statan.Web.Controllers
{
    public class HomeController : Controller
    {
        private readonly IAnalyzerResultRepository analyzerResultRepository;

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
            return View();
        }


        [HttpGet]
        public ActionResult Results()
        {
            var results = this.analyzerResultRepository.GetAll();
            return View(results);
        }

        [HttpPost]
        public JsonResult NewChart()
        {
            var results = this.analyzerResultRepository.GetAll()
                .Where(x => x.ProjectName == "thefuck");

            //Creating data  
            DataTable dt = new DataTable();
            dt.Columns.Add("Analyzer", System.Type.GetType("System.String"));
            dt.Columns.Add("Messages", System.Type.GetType("System.Int32"));

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