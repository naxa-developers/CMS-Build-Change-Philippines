from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('notification-update/', views.read_notification, name="notification_update"),
    path('project-create/', views.ProjectCreateView.as_view(), name="project_create"),
    # path('project-detail/<int:pk>/', views.ProjectDetailView.as_view(), name="project_detail"),
    path('project-update/<int:pk>/', views.ProjectUpdateView.as_view(), name="project_update"),
    path('project-delete/<int:pk>/', views.ProjectDeleteView.as_view(), name="project_delete"),
    path('user-create/', views.UserCreateView.as_view(), name="user_create"),
    path('user-list/', views.UserListView.as_view(), name="user_list"),
    path('dashboard/', views.Dashboard.as_view(), name="admin_dashboard"),
    path('project-dashboard/<int:project_id>', views.ProjectDashboard.as_view(), name="project_dashboard"),
    path('recent-updates/<int:project_id>', views.RecentUpdates.as_view(), name="recent_updates"),
    path('site-create/<int:project_id>/', views.SiteCreateView.as_view(), name="site_create"),
    path('site-update/<int:pk>/', views.SiteUpdateView.as_view(), name="site_update"),
    path('site-list/', views.SiteListView.as_view(), name="site_list"),
    path('site-delete/<int:pk>/', views.SiteDeleteView.as_view(), name="site_delete"),
    path('site-detail/<int:pk>/', views.SiteDetailView.as_view(), name="site_detail"),
    path('site-detail-js/<int:site_pk>/', views.SiteDetailTemplateView.as_view(), name="site_detail_js"),
    path('steps/<int:is_project>/<int:pk>/', views.SiteStepsView.as_view(), name="site-steps"),
    path('category-create/<int:project_id>/', views.CategoryFormView.as_view(), name="category_create"),
    path('category-list/<int:project_id>', views.CategoryListView.as_view(), name="category_list"),
    path('category-update/<int:pk>', views.CategoryUpdateView.as_view(), name="category_update"),
    path('category-delete/<int:pk>', views.CategoryDeleteView.as_view(), name="category_delete"),
    path('guideline-create/<int:project_id>/', views.MaterialFormView.as_view(), name="material_create"),
    path('guideline-update/<int:pk>/', views.MaterialUpdateView.as_view(), name="material_update"),
    path('guideline-delete/<int:pk>/', views.MaterialDeleteView.as_view(), name="material_delete"),
    path('guideline-detail/<int:pk>', views.MaterialDetailView.as_view(), name="material_detail"),
    path('guideline-list/<int:pk>', views.MaterialListView.as_view(), name="material_list"),
    path('site-guideline-create/<int:site_id>/', views.SiteMaterialFormView.as_view(), name="site_material_create"),
    path('site-guideline-list/<int:site_id>/', views.SiteMaterialListView.as_view(), name="site_material_list"),
    path('site-guideline-detail/<int:pk>/', views.SiteMaterialDetailView.as_view(), name="site_material_detail"),
    path('site-guideline-delete/<int:pk>/', views.SiteMaterialDeleteView.as_view(), name="site_material_delete"),
    path('site-report-detail/<int:pk>/', views.SiteReportDetailView.as_view(), name="site_report_detail"),
    path('document-create/<int:site_id>/', views.SiteDocumentFormView.as_view(), name="document_create"),
    path('document-list/<int:site_id>/', views.SiteDocumentListView.as_view(), name="document_list"),
    path('document-delete/<int:pk>/', views.SiteDocumentDeleteView.as_view(), name="document_delete"),
    path('substep-report-list/<int:pk>', views.SubstepReportListView.as_view(), name="substep_report_list"),
    path('substep-report-detail/<int:pk>', views.SubstepReportDetailView.as_view(), name="substep_report_detail"),
    path('substep-report-add', views.SubstepReportCreateView.as_view(), name="substep_report_add"),
    path('substep-report-edit/<int:pk>/', views.SubstepReportUpdateView.as_view(), name="substep_report_edit"),
    path('substep_report_delete/<int:pk>/', views.SubstepReportDeleteView.as_view(), name="substep_report_delete"),
    path('site-report-list/<int:pk>', views.SiteReportListView.as_view(), name="site_report_list"),
    path('site_report_delete/<int:pk>/', views.SiteReportDeleteView.as_view(), name="site_report_delete"),
    path('report-feedback/<int:pk>/', views.ReportFeedbackView.as_view(), name="report_feedback"),
    path('notification-list/', views.NotificationView.as_view(), name="notification_list"),
    path('user-profile-create/<int:pk>', views.UserProfileView.as_view(), name="user_profile"),
    path('user-profile-update/<int:pk>', views.	UserProfileUpdateView.as_view(), name="user_profile_update"),
    path('user-profile-detail/<int:pk>', views.UserProfileDetailView.as_view(), name="user_profile_detail"),

    path('project-material-photos/<int:project_id>', views.project_material_photos, name="project_material_photos"),
    path('project-personnel/<int:project_id>', views.ProjectPersonnelList.as_view(), name="project_personnel"),
    path('community-users/<int:project_id>', views.CommunityUsersList.as_view(), name="community_users"),

    path('site-documents-zip/<int:site_id>', views.site_documents_zip, name="site_documents_zip"),
    path('picture-list/', views.PictureList.as_view(), name="picture_list"),

    # Updated urls
    path('construction-substep-create/<int:project_id>/<int:step_id>', views.ConstructionSubstepCreate.as_view(), name="construction_substep_create"),
#     path('construction-substep-choose/<int:project_id>/<int:step_id>', views.ConstructionSubstepChoose.as_view(), name="construction_substep_choose"),
    path('construction-step-update/<int:pk>/', views.ConstructionStepUpdate.as_view(), name="construction_step_update"),
    path('construction-step-list/<int:project_id>/', views.ConstructionStepList.as_view(), name="construction_step_list"),
    path('construction-step-delete/<int:pk>/', views.ConstructionStepDelete.as_view(), name="construction_step_delete"),
    path('site-steps-create/<int:site_id>/', views.ConfigureSiteSteps.as_view(), name="site_steps_create"),
    path('site-sub-step-create/<int:site_id>/<int:step_id>', views.SiteSubStepCreate.as_view(), name="site_sub_steps_create"),
    path('configure-project-steps/<int:project_id>', views.ConfigureProjectSteps.as_view(), name="configure_project_steps"),
    path('construction-substeps-detail/<int:pk>/', views.ConstructionSubstepsDetail.as_view(), name="construction_substeps_detail"),
    path('construction-substeps-update/<int:pk>/', views.ConstructionSubstepsUpdate.as_view(), name="construction_substeps_update"),
    path('construction-site-steps-list/<int:site_id>/', views.ConstructionSitetepsList.as_view(), name="construction_site_steps_list"),
    path('construction-substeps-delete/<int:pk>/', views.ConstructionSubstepsDelete.as_view(),
         name="construction_substeps_delete"),
    path('construction-site-steps-delete/<int:pk>/', views.ConstructionSiteStepsDelete.as_view(),
         name="construction_site_steps_delete"),
    path('checklist-create/<int:site_id>/<int:step_id>/<int:substep_id>', views.ChecklistCreateView.as_view(), name="checklist_create"),
    path('checklist-update/<int:pk>/', views.ChecklistUpdateView.as_view(), name="checklist_update"),
    path('checklist-delete/<int:pk>/', views.ChecklistDeleteView.as_view(), name="checklist_delete"),

    path('checklist/<int:site_id>/<int:step_id>/<int:substep_id>/', views.ChecklistView.as_view(), name="checklist"),
    path('checklists-all/<int:site_id>', views.CheckListAllView.as_view(), name='checklist_all'),
    path('export/', views.export, name="export"),
    path('export-checklist-pdf/', views.ExportChecklistPdf, name="export_checklist_pdf"),
    path('export-report/', views.ExportReport, name="export_report"),
    path('export-report-pdf/', views.ExportPdf, name="export_report_pdf"),

    path('house-general-construction-materials-list', views.HousesAndGeneralConstructionMaterialsListView.as_view(), name="house_general_construction_materials_list"),
    path('house-general-construction-materials-detail/<int:pk>/', views.HousesAndGeneralConstructionMaterialsDetailView.as_view(), name="house_general_construction_materials_detail"),
    path('house-general-construction-materials-add/', views.HousesAndGeneralConstructionMaterialsCreateView.as_view(), name="house_general_construction_materials_add"),
    path('house-general-construction-materials-edit/<int:pk>/', views.HousesAndGeneralConstructionMaterialsUpdateView.as_view(), name="house_general_construction_materials_edit"),
    path('house-general-construction-materials-delete/<int:pk>/', views.HousesAndGeneralConstructionMaterialsDeleteView.as_view(), name="house_general_construction_materials_delete"),

    path('build-house/', views.BuildHouse.as_view(), name="build_house"),
    path('make-house-strong-list', views.MakeHouseStrongListView.as_view(), name="make_house_strong_list"),
    path('make-house-strong/<int:pk>/', views.MakesHouseStrongDetailView.as_view(), name="make_house_strong_detail"),
    path('make-house-strong-add/', views.MakesHouseStrongCreateView.as_view(), name="make_house_strong_add"),
    path('make-house-strong-edit/<int:pk>/', views.MakesHouseStrongUpdateView.as_view(), name="make_house_strong_edit"),
    path('make-house-strong-delete/<int:pk>/', views.MakesHouseStrongDeleteView.as_view(), name="make_house_strong_delete"),

    path('key-parts-house-list', views.KeyPartsOfHouseListView.as_view(), name="key_parts_house_list"),
    path('key-parts-house-detail/<int:pk>/', views.KeyPartsOfHouseDetailView.as_view(), name="key_parts_house_detail"),
    path('key-parts-house-add/', views.KeyPartsOfHouseCreateView.as_view(), name="key_parts_house_add"),
    path('key-parts-house-edit/<int:pk>/', views.KeyPartsOfHouseUpdateView.as_view(), name="key_parts_house_edit"),
    path('key-parts-house-delete/<int:pk>/', views.KeyPartsOfHouseDeleteView.as_view(), name="key_parts_house_delete"),

]