from django.contrib import admin
from .models import *

admin.site.register(Project)
admin.site.register(WO_PO)
admin.site.register(Company)
admin.site.register(LOIAttachments)
admin.site.register(Loa_PoAttachments)
admin.site.register(Electricity)
admin.site.register(ProjectMilestone)
admin.site.register(ProjectActivity)
admin.site.register(DrawingAndDesignAttachments)
admin.site.register(DrawingAndDesignManagement)
admin.site.register(DrawingAndDesignApprovedActions)
admin.site.register(DrawingAndDesignCommentedActions)
admin.site.register(DrawingAndDesignReSubmittedActions)

