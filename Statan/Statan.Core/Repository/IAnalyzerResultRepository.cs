using Statan.Core.Models;
using System.Collections.Generic;

namespace Statan.Core.Repository
{
    public interface IAnalyzerResultRepository
    {
        IEnumerable<AnalyzerResult> GetAll();
    }
}
