class API:
   def __init__(self, name, id, slug, httpMethod, type, relatedEntity, attributes, constraints):
      self.name = name
      self.id = id
      self.slug = slug
      self.httpMethod = httpMethod
      self.type = type
      self.relatedEntity = relatedEntity
      self.attributes = attributes
      self.constraints = constraints

   def exportAsJson(self):
      return {
         "name":self.name,
         "id":self.id,
         "slug":self.slug,
         "httpMethod":self.httpMethod,
         "type":self.type,
         "relatedEntity":self.relatedEntity,
         "attributes":self.attributes,
         "constraints":self.constraints
      }