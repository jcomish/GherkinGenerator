from Fitv.BrowserPool import BrowserPool
import Fitv
import settings


def before_step(context, step):
    Fitv.browser_pool.ContextSemaphore.acquire()
    Fitv.browser_pool.CurrentContext = context


def before_feature(context, feature):
    Fitv.browser_pool.claim_browser_from_pool(feature.name)


def after_feature(context, feature):
    Fitv.browser_pool.release_browser_from_pool(feature.name)


def before_all(context):
    Fitv.browser_pool = BrowserPool(context._runner.features, settings.MaxThreads, path=settings.DriverPath)


def after_all(context):
    Fitv.browser_pool.kill_browser_pool()
    exit(0)