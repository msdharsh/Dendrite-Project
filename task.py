class CreateTask(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    task = graphene.Field(lambda: Task)

    def mutate(self, info, name):
        task = TaskModel(name=name)
        db.session.add(task)
        db.session.commit()
        return CreateTask(task=task)

class UpdateTask(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        completed = graphene.Boolean()

    task = graphene.Field(lambda: Task)

    def mutate(self, info, id, name=None, completed=None):
        task = TaskModel.query.get(id)
        if name:
            task.name = name
        if completed is not None:
            task.completed = completed
        db.session.commit()
        return UpdateTask(task=task)

class DeleteTask(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        task = TaskModel.query.get(id)
        db.session.delete(task)
        db.session.commit()
        return DeleteTask(success=True)

class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()

schema = Schema(query=Query, mutation=Mutation)