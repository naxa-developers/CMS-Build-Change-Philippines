from django.urls import path, include
from django.conf.urls import url

from rest_framework import routers

from . import viewset
from .. import views
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet, FCMDeviceViewSet


router = routers.DefaultRouter()

router.register(r'users', viewset.UserViewSet)
router.register(r'project', viewset.ProjectViewSet, base_name='project-list')
router.register(r'checklist', viewset.ChecklistViewset, base_name='checklist-api')
router.register(r'step', viewset.StepViewset, base_name='step-api')
router.register(r'material', viewset.MaterialViewset, base_name='material-api')
router.register(r'report', viewset.ReportViewset, base_name='checklist-report')
router.register(r'images', viewset.ImagesViewset, base_name='images')
router.register(r'site-report', viewset.SiteReportsViewSet, base_name='site-report')
router.register(r'call-log', viewset.CallLogViewset, base_name='call_log')



urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.token),
    path('list-steps/<int:is_project>/<int:pk>/',
         viewset.ProjectSiteStepsViewSet.as_view({'get':  'list'})),
    path('step-list/<int:site>/', viewset.StepViewset.as_view({'get': 'list',}), name="api_steps"),
    #path('checklist-list/<int:step>/', viewset.ChecklistViewset.as_view({'get': 'list', }), name="api_checklist"),
    path('material-list/<int:project>/', viewset.MaterialViewset.as_view({'get': 'list', }), name="api_materials"),
    path('site-materials-list/<int:site>/', viewset.SiteMaterialViewSet.as_view({'get': 'list', }), name="api_site_materials"),
    path('site-report-list/<int:site>/', viewset.SiteReportViewSet.as_view({'get': 'list', }),
         name="api_site_report"),
    path('site-engineers/<int:site>/', viewset.SiteEngineerViewSet.as_view({'get': 'list', }),
         name="api_site_engineers"),
    path('site-documents/<int:site>/', viewset.SiteDocumentViewSet.as_view({'get': 'list', }), name="api_site_documents"),
    path('category-list/', viewset.CategoryViewSet.as_view({'get': 'list'})),

    path('construction-site-steps-update/', viewset.construction_site_steps_update),
    path('load-substeps/', viewset.load_substeps, name='ajax_load_substeps'),
    path('houses-and-general-construction/', viewset.houses_and_general_construction, name='houses_and_general_construction'),
    path('standard-school-design/', viewset.standard_school_design, name='standard_school_design'),
    url(r'^devices?$', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),

]