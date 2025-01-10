from config.database import db


class Queries:

    @staticmethod
    def commit(
    ) -> None:
        """
        Commit Database Changes
        """
        db.session.commit()

    def add_and_commit(
            self,
            models_object
    ) -> None:
        """
        Add Object and Save
        :param models_object: User or Strategy -> Some Instance of Models Class
        """

        db.session.add(models_object)
        self.commit()

    def delete_and_commit(
            self,
            models_object
    ) -> None:
        """
        Delete Object from DB
        :param models_object: User or Strategy -> Some Instance of Models Class
        """
        db.session.delete(models_object)
        self.commit()
