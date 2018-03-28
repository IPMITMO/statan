﻿using Statan.Core.Repository;
using System.Web.Mvc;

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

        public ActionResult About()
        {
            ViewBag.Message = "Your application description page.";

            return View();
        }

        public ActionResult Contact()
        {
            ViewBag.Message = "Your contact page.";

            return View();
        }
    }
}