# # from flask import render_template
# # from flask.views import View

# # class UserList(View):
# #     def dispatch_request(self):
# #         users = ""
# #         # users = User.query.all()
# #         return render_template("users.html", objects=users)

# # app.add_url_rule("/users/", view_func=UserList.as_view("user_list"))

# class ListView(View):
#     def __init__(self, model, template):
#         self.model = model
#         self.template = template

#     def dispatch_request(self):
#         items = self.model.query.all()
#         return render_template(self.template, items=items)
    
# app.add_url_rule(
#     "/users/",
#     view_func=ListView.as_view("user_list", User, "users.html"),
# )
# app.add_url_rule(
#     "/stories/",
#     view_func=ListView.as_view("story_list", Story, "stories.html"),
# )

# class DetailView(View):
#     def __init__(self, model):
#         self.model = model
#         self.template = f"{model.__name__.lower()}/detail.html"

#     def dispatch_request(self, id)
#         item = self.model.query.get_or_404(id)
#         return render_template(self.template, item=item)

# app.add_url_rule(
#     "/users/<int:id>",
#     view_func=DetailView.as_view("user_detail", User)
# )