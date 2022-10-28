from django.contrib import admin
from django.urls import path
from .zoya_site.views import User, UpdateExp, UpdateLvl, RankingAPI, UserActive, UserInactive

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/<int:dcid>/', User.as_view(), name='user'),
    path('api/exp/update/', UpdateExp.as_view(), name='exp_update'),
    path('api/lvl/update/', UpdateLvl.as_view(), name='lvl_update'),
    path('api/ranking/', RankingAPI.as_view(), name='ranking_api'),
    path('api/user/active/', UserActive.as_view(), name='active_user'),
    path('api/user/inactive/', UserInactive.as_view(), name='inactive_user'),
    # path('/', Ranking.as_view(), name='ranking'),
]
