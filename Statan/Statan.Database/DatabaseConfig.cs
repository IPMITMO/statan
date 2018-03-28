using Statan.Core.Repository;
using Statan.Database.Repository;
using Unity;

namespace Statan.Database
{
    public static class DatabaseConfig
    {
        public static void RegisterTypes(IUnityContainer container)
        {
            container.RegisterType<IAnalyzerResultRepository, AnalyzerResultRepository>();
        }
    }
}
