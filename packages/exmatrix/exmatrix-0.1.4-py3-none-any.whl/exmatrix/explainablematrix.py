from exmatrix.rulevectormatrix import RuleVectorMatrix
from exmatrix.explanation import Explanation
from sklearn import tree
import bisect
import numpy as np
from scipy.cluster import hierarchy
import csv
import scipy.sparse as ssp











class ExplainableMatrix( RuleVectorMatrix ):

	
	def __init__( self, precision = 2, **kwargs ):


		self.precision = precision

		
		self._instances_names = None
		self._instances_map_category = None
		self._instances_map_delta = None
		self._rules_features_diameter = None
		self._rules_alg1 = None


		super().__init__( **kwargs )
		

		if ( 'file' in kwargs ): self.load( kwargs[ 'file' ] )

		
		











	def rule_extration( self, skl_trees, X, y, feature_importances = None, calc_support_coverage = False, calc_diameter = True, n_jobs = 1 ):

		X = self._check_input_X( X )
		y = self._check_input_y( y )


		n_trees = len( skl_trees )

		self.feature_values_min_ = np.array( [ np.amin( X[:, i] ) for i in range( X.shape[1] ) ] )
		self.feature_values_max_ = np.array( [ np.amax( X[:, i] ) for i in range( X.shape[1] ) ] )


		for c in np.unique( y ):
			self.class_instances_count_[ c ] = np.count_nonzero( y == c )
		self.class_instances_count_ = np.array( self.class_instances_count_ )


		self.feature_importances_ = feature_importances		
		

		if n_trees == 1:
			self.__type = 'tree'
		else:
			self.__type = 'forest'


		if self._verbose > 0: print( 'starting rules extration process ...' )

		rules_matrix = []

		for i in range( n_trees ):

			if self._verbose > 0: print( 'tree ', i )
			
			self.__path_to_rule( skl_trees[ i ].tree_, tree_id = i, node = 0, rule = super()._get_empty_rule(), rules_matrix = rules_matrix )
			
		
		super()._set_rules_matrix( rules_matrix )

		self.features_used_ = np.array( self.features_used_ )

		if self._verbose > 0: print( 'rules extration conclued' )


		if ( calc_support_coverage ): self.calc_support_coverage( X, y, n_jobs )


		if calc_diameter: self.calc_rules_features_diameter()











	def __path_to_rule( self, skl_tree, tree_id , node, rule, rules_matrix ):


		left_child = skl_tree.children_left[ node ]
		right_child = skl_tree.children_right[ node ]

		
		if ( left_child == tree._tree.TREE_LEAF ):

			
			rule[ self.ID ] = self.n_rules_
			self.n_rules_ += 1

			rule[ self.MODEL ] = tree_id
			rule[ self.NODE ] = node
		
			
			node_value = skl_tree.value[ node ][0]
			target =  np.argmax( node_value )
			root_node_value = skl_tree.value[0][0]
			node_value_sum = node_value.sum()

			rule[ self.CLASS ] = target
			rule[ self.SUPPORT ] = node_value[ target ] / root_node_value[ target ] # assuming bootstrap = False
			rule[ self.COVERAGE ] = node_value_sum / root_node_value.sum() # assuming bootstrap = False
			rule[ self.CERTAINTY ] = node_value[ target ] / node_value_sum
			rule[ self.VALUETOTAL ] = node_value_sum			
				
			

			rule_copy = list( rule )
			

			n_predicates = 0
			ranges_diameter_sum = 0

			for f in range( self.n_features_ ):

				a = f * 2
				b = a + 1

				if( ( rule_copy[ a ] != 'NaN' ) and ( rule_copy[ b ] == 'NaN' ) ):

					
					rule_copy[ b ] = self.feature_values_max_[ f ]

					n_predicates += 1

					ranges_diameter_sum += abs( ( rule_copy[ b ] - rule_copy[ a ] ) / ( self.feature_values_max_[ f ] - self.feature_values_min_[ f ] ) )


				elif( ( rule_copy[ a ] == 'NaN' ) and ( rule_copy[ b ] != 'NaN' ) ):

					
					rule_copy[ a ] = self.feature_values_min_[ f ]

					n_predicates += 1

					ranges_diameter_sum += abs( ( rule_copy[ b ] - rule_copy[ a ] ) / ( self.feature_values_max_[ f ] - self.feature_values_min_[ f ] ) )


				elif( ( rule_copy[ a ] != 'NaN' ) and ( rule_copy[ b ] != 'NaN' ) ):

					
					n_predicates += 1

					ranges_diameter_sum += abs( ( rule_copy[ b ] - rule_copy[ a ] ) / ( self.feature_values_max_[ f ] - self.feature_values_min_[ f ] ) )


				else:

					rule_copy[ b ] = 0
					rule_copy[ a ] = 0


			rule_copy[ self.NPREDICATES ] = n_predicates
			rule_copy[ self.RANGESDIAMETERMEAN ] = ranges_diameter_sum / n_predicates
			
			rule_copy[ self.AUX1 ] = 0
			rule_copy[ self.AUX2 ] = 0
			rule_copy[ self.AUX3 ] = 0


			for c in range( self.n_classes_ ):

				rule_copy[ self.VALUEC0 + c ] = node_value[ c ]


			if self._verbose > 1: print( 'rule extracted ' + str( self.n_rules_ ), rule_copy )	
			rules_matrix.append( rule_copy )

					
		else:


			f = skl_tree.feature[ node ]

			if f not in self.features_used_: # otimizar a procura na lista uma vez que esta estar ordenada
				bisect.insort( self.features_used_, f )
 
			
			threshold = skl_tree.threshold[ node ]	


			a = f * 2
			b = a + 1


			aux_sup	= rule[ b ]
			if( ( rule[ b ] == 'NaN' ) or ( rule[ b ] > threshold ) ):
				aux_sup	= rule[ b ]
				rule[ b ] = threshold 

			self.__path_to_rule( skl_tree, tree_id, left_child, rule, rules_matrix )

			rule[ b ] = aux_sup



			aux_inf = rule[ a ]
			if( ( rule[ a ] == 'NaN' ) or ( rule[ a ] < threshold ) ):
				aux_inf = rule[ a ]

				eps = 0.0000001e-38 # a = np.finfo(np.float32) # a >>> finfo(resolution=1e-06, min=-3.4028235e+38, max=3.4028235e+38, dtype=float32) # a,tiny >>> 1.1754944e-38

				if threshold >= 0.0: rule[ a ] = threshold + eps
				else: rule[ a ] = threshold - eps

			self.__path_to_rule( skl_tree, tree_id, right_child, rule, rules_matrix )

			rule[ a ] = aux_inf











	def rules_to_bars3d( self ):

		rules = np.array( range( self.n_rules_ ) )
		features = super()._get_features_used( rules )

		if( features.shape[0] != 3 ):
			raise ValueError('number of features must be 3')


		bars3d = []

		for r in rules:
			
			bar3d = []
			post = []
			size = []
			for f in features:

				a = f * 2
				b = a + 1

				if( ( self.rules_matrix_[ r, a ] != 0 ) and ( self.rules_matrix_[ r, b ] != 0 ) ):

					post.append( self.rules_matrix_[ r, a ] )
					size.append( abs( self.rules_matrix_[ r, b ] - self.rules_matrix_[ r, a ] ) )

				else:

					post.append( self.feature_values_min_[ f ] )
					size.append( abs( self.feature_values_max_[ f ] - self.feature_values_min_[ f ] ) )

			size.append( self.rules_matrix_[ r, self.CLASS ] )		
			bar3d = post
			bar3d.extend( size )

			bars3d.append( bar3d )


		return np.array( bars3d )











	def calc_rules_features_diameter( self, normalized = True ):

		if self._verbose > 0: print( 'starting rules features diameter calculation ...' )

		self._rules_features_diameter = ssp.lil_matrix( ( self.n_rules_, self.n_features_ ) )


		for rule in range( self.n_rules_ ):

			if self._verbose > 0: print( 'calculating features diameter of rule: ', rule )

			features_calc = []

			for f_ab in self.rules_matrix_[ rule, :( self.n_features_ * self._shift ) ].nonzero()[ 1 ]:

				f = super()._feature_map( f_ab )
				if f not in features_calc: 

					features_calc.append( f )

					a = f * 2
					b = a + 1

					diameter = self.rules_matrix_[ rule, b ] - self.rules_matrix_[ rule, a ]

					if normalized: diameter /= ( self.feature_values_max_[ f ] - self.feature_values_min_[ f ] )


					self._rules_features_diameter[ rule, f ] = diameter


		if self._verbose > 0: print( 'rules features diameter calculated' )










	
	def __order_by_link( self, matrix, method, optimal_ordering ):

		try:

			link_mat = hierarchy.linkage( matrix, method = method, optimal_ordering = optimal_ordering )
			indexes = hierarchy.leaves_list( link_mat )			
			return indexes

		except Exception as e:
			print( e )
			return np.array( range( matrix.shape[ 0 ] ) )

	









	def order_rows( self, rows, criteria, cols,

		link_method = 'complete', link_optimal_ordering = True, row_values = None ):

		
		if criteria == 'support':
			indexes = np.argsort( self.rules_matrix_[ rows, self.SUPPORT ].toarray()[ :, 0 ] )[ ::-1 ]
			return indexes

		elif criteria == 'certainty':
			indexes = np.argsort( self.rules_matrix_[ rows, self.CERTAINTY ].toarray()[ :, 0 ] )[ ::-1 ]	
			return indexes

		elif criteria == 'class & support':
			crt_1 = self.rules_matrix_[ rows, self.CLASS ].toarray()[ :, 0 ]
			crt_2 = -1 * self.rules_matrix_[ rows, self.SUPPORT ].toarray()[ :, 0 ]
			indexes = np.lexsort( ( crt_2, crt_1 ) )
			return indexes

		elif criteria == 'class & certainty':
			crt_1 = self.rules_matrix_[ rows, self.CLASS ].toarray()[ :, 0 ]
			crt_2 = -1 * self.rules_matrix_[ rows, self.CERTAINTY ].toarray()[ :, 0 ]
			indexes = np.lexsort( ( crt_2, crt_1 ) )
			return indexes
		
		elif criteria == 'range-link':
			rc_sel = np.ix_( rows, cols )
			indexes = self.__order_by_link( self._rules_features_diameter[ rc_sel ].toarray(), link_method, link_optimal_ordering )
			return indexes

		elif criteria == 'delta change':
			indexes = np.argsort( row_values[ rows ] )
			return indexes

		else: return np.array( [ ] )

	









	def order_cols( self, cols, criteria, rows,

		link_method = 'complete', link_optimal_ordering = True ):

		
		if criteria == 'importance':

			if self.feature_importances_ is not None:
				indexes = np.argsort( self.feature_importances_[ cols ] )[ ::-1 ]
				return indexes
			else: return cols

		elif criteria == 'range-link':
			rc_sel = np.ix_( rows, cols )
			indexes = self.__order_by_link( self._rules_features_diameter[ rc_sel ].toarray().T, link_method, link_optimal_ordering )
			return indexes







	



	def explanation( self, exp_type = 'global', x_k = None, r_model = None, r_node = None, r_support_min = None,  r_certainty_min = None, r_class = None, r_order = 'raw', f_order = 'raw', info_text = None ):


		if info_text is None: info_text = '\n'
		else: info_text += '\n'


		cumulative_voting = None
		old_rules = None
		old_rule_certainties = None

		class_names = None


		if exp_type == 'global': 
			
			rules = np.array( range( self.n_rules_ ) )
			features = self.features_used_

			class_names = self.class_names_

			info_text += 'type ' + exp_type + '\n'


		elif exp_type == 'local':

			y_pred, proba, rules, closest_rules, rules_delta_sum = super().predict_x( x_k, closest_rules = True, counterfactual_class = 'all' )
			
			rules = np.hstack( ( rules, closest_rules ) )
			features = super()._get_features_used( rules )			

			info_text += 'type ' + exp_type + '\n'


		elif exp_type == 'local-all':

			_, proba, _, _, rules_delta_sum = super().predict_x( x_k, closest_rules = True, counterfactual_class = 'all' )

			rules = np.array( range( self.n_rules_ ) )
			features = super()._get_features_used( rules )			

			info_text += 'type ' + exp_type + '\n'


		elif exp_type == 'local-used':

			y_pred, proba, rules = super().predict_x( x_k )
			features = super()._get_features_used( rules )			

			info_text += 'type ' + exp_type + '\n'


		elif exp_type == 'local-closest':

			y_pred, proba, old_rules, rules, rules_delta_sum = super().predict_x( x_k, closest_rules = True )
			features = super()._get_features_used( rules )

			info_text += 'type ' + exp_type + '\n'


		
		if r_model is not None:

			indexes = np.argwhere( self.rules_matrix_[ rules, self.MODEL ].toarray()[ :, 0 ] == r_model )[ :, 0 ]
			rules = rules[ indexes ]
			if old_rules is not None: old_rules = old_rules[ indexes ]
			info_text += 'model ' + str( r_model ) + '\n'


		if r_node is not None:

			indexes = np.argwhere( self.rules_matrix_[ rules, self.NODE ].toarray()[ :, 0 ] == r_node )[ :, 0 ]
			rules = rules[ indexes ]
			if old_rules is not None: old_rules = old_rules[ indexes ]
			info_text += 'node ' + str( r_node ) + '\n'


		if r_support_min is not None:	

			indexes = np.argwhere( self.rules_matrix_[ rules, self.SUPPORT ].toarray()[ :, 0 ] >= r_support_min )[ :, 0 ]
			rules = rules[ indexes ]
			if old_rules is not None: old_rules = old_rules[ indexes ]
			info_text += 'support >= ' + str( r_support_min ) + '\n'


		if r_certainty_min is not None:	

			indexes = np.argwhere( self.rules_matrix_[ rules, self.CERTAINTY ].toarray()[ :, 0 ] >= r_certainty_min )[ :, 0 ]
			rules = rules[ indexes ]
			if old_rules is not None: old_rules = old_rules[ indexes ]
			info_text += 'certainty >= ' + str( r_certainty_min ) + '\n'


		if r_class is not None:	

			indexes = np.argwhere( self.rules_matrix_[ rules, self.CLASS ].toarray()[ :, 0 ] == r_class )[ :, 0 ]
			rules = rules[ indexes ]
			if old_rules is not None: old_rules = old_rules[ indexes ]
			info_text += 'class ' + self.class_names_[ r_class ] + '\n'


		if ( r_model is not None ) or ( r_node is not None ) or ( r_support_min is not None ) or ( r_certainty_min is not None ) or ( r_class is not None ): 
			features = super()._get_features_used( rules )


			

		if f_order != 'raw':
			indexes = self.order_cols( features, f_order, rules )
			features = features[ indexes ]


	

		if r_order != 'raw':

			if ( r_order == 'delta change' ) and ( ( exp_type == 'local') or ( exp_type == 'local-all') or ( exp_type == 'local-closest') ): 

				indexes = self.order_rows( rules, r_order, features, row_values = rules_delta_sum )

			else: indexes = self.order_rows( rules, r_order, features )
			
			rules = rules[ indexes ]

			if old_rules is not None: old_rules = old_rules[ indexes ]

		




		features_used_ab = super()._to_features_ab( features )
		rc_sel = np.ix_( rules, features_used_ab )



		rule_labels = [ 'r ' + str( r + 1 ) for r in rules ]



		rule_certainties = self.rules_matrix_[ rules, self.VALUEC0: ].toarray() / self.rules_matrix_[ rules, self.VALUETOTAL ].toarray()

		
		
		if exp_type == 'local-used': 
			cumulative_voting = super()._aggregate_voting( rules )
			proba = cumulative_voting[ -1 ]

		elif exp_type == 'local-closest': old_rule_certainties = self.rules_matrix_[ old_rules, self.VALUEC0: ].toarray() / self.rules_matrix_[ old_rules, self.VALUETOTAL ].toarray()



		if ( exp_type == 'local' ) or ( exp_type == 'local-all' ) or ( exp_type == 'local-used' ) or ( exp_type == 'local-closest' ):

			class_names = []
			for c in range( self.class_names_.shape[ 0 ] ):
				class_names.append( self.class_names_[ c ] + ' | ' + str( np.round( proba[ c ], decimals = 2 ) ) )
			class_names = np.array( class_names )

		
		if x_k is None:

			if self.feature_importances_ is not None: feature_labels = [ self.feature_names_[ f ] + ' | ' + str( np.round( self.feature_importances_[ f ], decimals = self.precision ) ) for f in features ]
			else: feature_labels = self.feature_names_[ features ]

		else: 
			feature_labels = [ str( np.round( x_k[ f ], decimals = self.precision ) ) + ' | ' + self.feature_names_[ f ] + ' | ' + str( np.round( self.feature_importances_[ f ], decimals = self.precision ) ) for f in features ]

			x_k = x_k[ features ]



		if self.feature_importances_ is not None: feature_importances = self.feature_importances_[ features ]
		else: feature_importances = None 



		info_text += '\nrules ' + str( rules.shape[ 0 ] ) + '\nby ' + r_order + '\n'
		info_text += '\nfeatures ' + str( features.shape[ 0 ] ) + '\nby ' + f_order



		return Explanation( exp_type = exp_type, rules  = rules, features = features, matrix =  self.rules_matrix_[ rc_sel ].toarray(),
			
			rule_classes = self.rules_matrix_[ rules, self.CLASS ].toarray()[ :, 0 ].astype( int ),  
			rule_labels = rule_labels, 
			rule_supports = self.rules_matrix_[ rules, self.SUPPORT ].toarray()[ :, 0 ],
			rule_certainties = rule_certainties,
			cumulative_voting = cumulative_voting,
			old_rule_certainties = old_rule_certainties,
			
			feature_labels = feature_labels, 
			feature_importances = feature_importances, 
			feature_values_min = self.feature_values_min_[ features ], 
			feature_values_max = self.feature_values_max_[ features ], 
			
			class_names = class_names,			
			x_k = x_k,
			info_text = info_text )











	def save( self, file, rules = None, npz_format = True ):

		super().save_rules_matrix( file, rules, npz_format )











	def load( self, file, npz_format = True, calc_diameter = True  ):

		super().load_rules_matrix( file, npz_format )

		if calc_diameter == True: self.calc_rules_features_diameter()