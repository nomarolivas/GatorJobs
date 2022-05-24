from . import db


class User(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'Student'
    Student_id = db.Column(
        db.String(45),
        primary_key=True
    )
    Username = db.Column(
        db.String(45),
        index=False,
        unique=True,
        nullable=False
    )
    Password = db.Column(
        db.String(45),
        index=False,
        unique=False,
        nullable=False
    )
    Name = db.Column(
        db.String(45),
        index=True,
        unique=False,
        nullable=False
    )
    Email = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )
    Photo_path = db.Column(
        db.String(45),
        index=True,
        unique=False,
        nullable=False
    )
    Address = db.Column(
        db.String(45),
        index=True,
        unique=False,
        nullable=False
    )
    Phone_number = db.Column(
        db.Integer,
        index=True,
        unique=True,
        nullable=False
    )
    Date_of_birth = db.Column(
        db.String(45),
        index=False,
	unique=False,
        nullable=False
    )
    Pin_code = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    Links = db.Column(
        db.String(45),
        index=True,
        unique=True,
        nullable=False
    )
    Skills = db.Column(
        db.String(45),
        index=True,
        unique=False,
        nullable=False
    )
    Languages_spoken = db.Column(
        db.String(45),
        index=True,
        unique=False,
        nullable=False
    )
    Proficiency = db.Column(
        db.Integer,
        index=True,
        unique=False,
        nullable=False
    )
    Objectives = db.Column(
        db.String(45),
        index=True,
        unique=False,
        nullable=True
    )
    Recommendation_letter = db.Column(
        db.String(45),
        index=True,
        unique=True,
        nullable=True
    )
    Category = db.Column(
        db.String(45),
        index=True,
        unique=False,
        nullable=False
    )
    Permissions = db.Column(
        db.String(45),
        index=True,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)
