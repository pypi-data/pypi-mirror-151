from exmatrix.drawmatrix import draw_range_matrix











class Explanation( ):


	def __init__( self, exp_type, rules, features, matrix, 

		rule_classes, rule_labels, rule_supports, rule_certainties, cumulative_voting, old_rule_certainties,

		feature_labels, feature_importances, feature_values_min, feature_values_max, class_names, x_k = None, info_text = None ):

		self.svg_draw_ = None

		self.exp_type = exp_type

		self.rules = rules
		self.features = features
		self.matrix = matrix

		self.rule_classes = rule_classes
		self.rule_labels = rule_labels
		self.rule_supports = rule_supports
		self.rule_certainties = rule_certainties
		self.cumulative_voting = cumulative_voting
		self.old_rule_certainties = old_rule_certainties

		self.feature_labels = feature_labels
		self.feature_importances = feature_importances
		self.feature_values_min = feature_values_min
		self.feature_values_max = feature_values_max

		self.class_names = class_names
		self.x_k = x_k
		self.info_text = info_text











	def create_svg( self, draw_row_labels = False, draw_col_labels = False, **kwargs ):

		self.row_labels = None
		if draw_row_labels: self.row_labels = self.rule_labels

		self.col_labels = None
		if draw_col_labels: self.col_labels = self.feature_labels


		self.rows_right_legend_2_title = None
		self.rows_right_legend_2 = None
		if self.exp_type == 'local-used':

			self.rows_right_legend_2_title = 'Cumulative Voting'
			self.rows_right_legend_2 = self.cumulative_voting

		elif self.exp_type == 'local-closest':

			self.rows_right_legend_2_title = 'Old-Rule Certainty'
			self.rows_right_legend_2 = self.old_rule_certainties


		

		self.svg_draw_ = draw_range_matrix( 

			matrix = self.matrix, 
			col_values_min = self.feature_values_min, 
			col_values_max = self.feature_values_max, 
			matrix_row_categories = self.rule_classes, 
			category_names = self.class_names, 
			
			row_labels = self.row_labels,
			col_labels = self.col_labels,

			cols_top_legend_title = 'Feature Importance',
			cols_top_legend = self.feature_importances,
			rows_left_legend_title = 'Rule Support',
			rows_left_legend = self.rule_supports, 
			rows_right_legend_1_title = 'Rule Certainty',
			rows_right_legend_1 = self.rule_certainties,
			rows_right_legend_2_title = self.rows_right_legend_2_title,
			rows_right_legend_2 = self.rows_right_legend_2,

			x_k = self.x_k,
			info_text = self.info_text,

			**kwargs )











	def save( self, file, pixel_scale = 'default' ):

		if '.png' in file:

			if pixel_scale != 'default': self.svg_draw_.setPixelScale( pixel_scale )
			else: self.svg_draw_.setPixelScale( 2 )

			self.svg_draw_.savePng( file )

			self.svg_draw_.setPixelScale( 1 )

		elif '.svg' in file:

			if pixel_scale != 'default': self.svg_draw_.setPixelScale( pixel_scale )
			else: self.svg_draw_.setPixelScale( 1 ) 

			self.svg_draw_.saveSvg( file )

			self.svg_draw_.setPixelScale( 1 )
			











	def display_jn( self, display_type = 'svg', pixel_scale = 'default' ):

		if display_type == 'svg':

			if pixel_scale != 'default': self.svg_draw_.setPixelScale( pixel_scale )
			else: self.svg_draw_.setPixelScale( 0.45 )

			return self.svg_draw_

		elif display_type == 'png':

			if pixel_scale != 'default': self.svg_draw_.setPixelScale( pixel_scale )
			else: self.svg_draw_.setPixelScale( 2 ) 

			return self.svg_draw_.rasterize()











	def to_dict( self ):

		result_dict = {}

		result_dict['matrix'] = self.matrix.tolist()

		result_dict['col_values_min'] = self.feature_values_min.tolist()
		result_dict['col_values_max'] = self.feature_values_max.tolist()

		result_dict['row_categories'] = self.rule_classes.tolist()
		result_dict['category_names'] = self.class_names.tolist()
		result_dict['row_labels'] = self.row_labels
		result_dict['rows_left_legend'] = self.rule_supports.tolist() 
		result_dict['rows_right_legend_1'] = self.rule_certainties.tolist()
		result_dict['rows_right_legend_2'] = self.rows_right_legend_2.tolist()
		result_dict['rows_right_legend_2_title'] = self.rows_right_legend_2_title

		result_dict['col_labels'] = self.col_labels
		result_dict['cols_top_legend'] = self.feature_importances.tolist()


		if self.x_k is not None: result_dict['x_k'] = self.x_k.tolist()
		else: result_dict['x_k'] = None
		result_dict['info_text'] = self.info_text


		return result_dict