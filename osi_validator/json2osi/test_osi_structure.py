import unittest

from osistructure import OsiStructure

class TestBooleanValues(unittest.TestCase):

	def test_isClassEnum(self):
		osi = OsiStructure()
		self.assertFalse(osi.isClassEnum('StationaryObject'))
		self.assertFalse(osi.isClassEnum('StationaryObject.Classification'))
		self.assertTrue(osi.isClassEnum(
							'StationaryObject.Classification.Color'))


class TestGetFieldType(unittest.TestCase):
	"""This class tests the getting the properties of osi classes"""

	def test_isFieldReapeted(self):
		osi = OsiStructure()
		self.assertFalse(osi.isFieldRepeted('StationaryObject','id'))
		self.assertTrue(osi.isFieldRepeted('BaseStationary','base_polygon'))

	def test_isFieldPrimitive(self):
		osi = OsiStructure()
		self.assertFalse(osi.isFieldPrimitive('StationaryObject','id'))
		self.assertTrue(osi.isFieldPrimitive('Identifier','value'))

	def test_getFieldClassification(self):
		osi = OsiStructure()
		self.assertEqual(osi.getFieldClassification
					('StationaryObject', 'id'),'COMPOSITE_SINGLE')
		self.assertEqual(osi.getFieldClassification
					('BaseStationary','base_polygon'),'COMPOSITE_ITERABLE')
		self.assertEqual(osi.getFieldClassification
					('Identifier','value'),'PRIMITIVE_SINGLE')
		self.assertEqual(osi.getFieldClassification
					('StationaryObject.Classification','color'),'ENUMERATION')

	def test_getFieldType(self):
		osi = OsiStructure()
		
		self.assertEqual(
			osi.getFieldType('StationaryObject','id'),'Identifier')

		self.assertEqual(osi.getFieldType('StationaryObject.Classification','type'),'StationaryObject.Classification.Type')


if __name__ == '__main__':
    unittest.main()