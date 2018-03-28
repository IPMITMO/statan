using Statan.Core.Models;
using Statan.Core.Repository;
using Statan.Database.Entities;
using System.Collections.Generic;
using System.Linq;

namespace Statan.Database.Repository
{
    internal sealed class AnalyzerResultRepository 
        : DatabaseRepository<AnalyzerResultEntity>, IAnalyzerResultRepository
    {
        public IEnumerable<AnalyzerResult> GetAll()
        {
            return this.Get().Select(this.ToModel);
        }

        private AnalyzerResult ToModel(AnalyzerResultEntity entity)
        {
            return new AnalyzerResult
            {
                Id = entity.Id,
                Origin = entity.Origin,
                Language = entity.Language,
                LanguageVersion = entity.LanguageVersion,
                ProjectName = entity.ProjectName,
                ProjectVersion = entity.ProjectVersion,
                SourceFilePath = entity.SourceFilePath,
                Message = entity.Message,
                StartLine = entity.StartLine,
                Severity = entity.Severity,
                Diffs = entity.Diffs,
                Confidence = entity.Confidence,
                Params = entity.Params
            };
        }
    }
}
