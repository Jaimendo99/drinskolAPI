from marshmallow import Schema, fields


class SimpleUserSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    username = fields.Str(required=True)

class BaseUserSchema(SimpleUserSchema):
    password = fields.Str(required=True, load_only=True)
    email = fields.Email(required=True)
    birth_date = fields.Date(required=True)
    image_src = fields.Str(required=True)
    is_admin = fields.Boolean(required=True)

class UserSchema(BaseUserSchema):
    experiences = fields.List(fields.Nested('ExperienceSchema'))
    drinks = fields.List(fields.Nested('BaseDrinkSchema'), dump_only=True)

class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)



class SimpleDrinkSchema(Schema):
    id = fields.Integer(required=True, dump_only=True)
    name = fields.Str(required=True)

class BaseDrinkSchema(SimpleDrinkSchema):
    id = fields.Integer(required=True, dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    alcohol_porcentage = fields.Float(required=True)
    image_src = fields.Str(required=True)

class DrinkSchema(BaseDrinkSchema):
    tags =fields.List(fields.Nested('BaseTagSchema'))

class GetDrinkSchema(BaseDrinkSchema):
    tags = fields.List(fields.Nested('BaseTagSchema'))
    experiences = fields.List(fields.Nested('ExperienceSchema'))
    recipes = fields.List(fields.Nested('RecipeSchema'))

class BaseIngridientSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    alcohol_porcentage = fields.Float(required=True)
    image_src = fields.Str(required=True)



class IngridientSchema(BaseIngridientSchema):
    drinks = fields.List(fields.Nested('BaseDrinkSchema'))

class BaseTagSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    name = fields.Str(required=True)

class TagSchema(BaseTagSchema):
    drinks = fields.List(fields.Nested('BaseDrinkSchema'))


class BaseExperienceSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    rating = fields.Int(required=True)
    comment = fields.Str(required=True)
    wishlist = fields.Boolean(required=True)


class ExperienceSchema(BaseExperienceSchema):
    user_id = fields.Int(required=True)
    drink_id = fields.Int(required=True)


class detailExperienceSchema(BaseExperienceSchema):
    user = fields.Nested('SimpleUserSchema')
    drink = fields.Nested('SimpleDrinkSchema')


class BaseRecipeSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    quantity = fields.Float(required=True)
    order = fields.Int(required=True)


class CreateRecipeEntrySchema(BaseRecipeSchema):
    drink_id = fields.Int(required=True)
    ingridient_id = fields.Int(required=True)


class RecipeSchema(BaseRecipeSchema):
    drink_id = fields.Int(required=True)
    ingridient = fields.Nested('BaseIngridientSchema')



class CreateTagDrinkSchema(Schema):
    drink_id = fields.Int(required=True)
    tag_id = fields.Int(required=True)

class TagDrinkSchema(Schema):
    id = fields.Int(required=True, dump_only=True)

    drink = fields.Nested('BaseDrinkSchema')
    tag = fields.Nested('BaseTagSchema')
