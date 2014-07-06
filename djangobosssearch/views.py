'''
The BOSS search / results view.
'''

from django.conf import settings
try:
    from django.shortcuts import render
except ImportError:
    from django.views.generic.simple import direct_to_template as render

from djangobosssearch.paginator import ResultsetPaginator
from djangobosssearch.providers.boss import BossWebSearchProvider, \
    BossSiteSearchProvider


def bosssearch(request):
    '''
    Perform a search using the BossWebSearchProvider.
    '''
    if 'q' in request.POST and request.POST['q'].strip():
        market = getattr(settings, 'BOSS_SEARCH_MARKET', 'en-us')
        rpp = getattr(settings, 'BOSS_RESULTS_PER_PAGE', 50)
        if hasattr(settings, 'BOSS_SITE_SEARCH_DOMAIN'):
            provider = BossSiteSearchProvider(settings.BOSS_API_KEY,
                                              settings.BOSS_API_SECRET,
                                              settings.BOSS_SITE_SEARCH_DOMAIN,
                                              market)
        else:
            provider = BossWebSearchProvider(settings.BOSS_API_KEY,
                                             settings.BOSS_API_SECRET,
                                             market)
        resultset = provider.search(request.POST['q'])
        paginator = ResultsetPaginator(resultset, rpp)
        if 'page-num' in request.POST and request.POST['page-num'].strip():
            page_obj = paginator.page(request.GET.get('page', request.POST['page-num']))
        else:
            page_obj = paginator.page(request.GET.get('page', request.POST['page-num']))
        if request.is_ajax():
            return render(request, 'bosssearch/inclusion/results.html', {
                'resultset': resultset,
                'paginator': paginator,
                'page_obj': page_obj,
            })
        else:
            return render(request, 'bosssearch/results.html', {
                'resultset': resultset,
                'paginator': paginator,
                'page_obj': page_obj,
            })
    return render(request, 'bosssearch/form.html')
