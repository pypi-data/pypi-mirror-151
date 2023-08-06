import drawSvg as draw
import numpy as np











n_rows_ = n_cols_ = None
margin_top_ = margin_right_ = margin_bottom_ = margin_left_ = None
inner_width_ = inner_height_ = None
col_values_max_ = col_values_min_ = None











def scale( x, x_min, x_max, new_min, new_max ):
	return ( ( ( ( new_max - new_min ) * ( x - x_min ) ) / ( x_max - x_min ) ) + new_min )



def row_scale( r ):
	return scale( r, 0, n_rows_, 0, inner_height_ )



def col_scale( c ):
	return scale( c, 0, n_cols_, 0, inner_width_ )



def draw_row_label( g, r, label, font_size, rec_height, pad ):
	g.append( draw.Text( label, font_size, -pad, -( row_scale( r ) + ( rec_height / 2 ) + ( font_size / 2 ) ), text_anchor = 'end', fill = '#000000' ) )



def draw_col_label( g, c, label, font_size, degrees, pad ):

	if degrees == 0: text_anchor = 'middle'
	else: text_anchor = 'start'

	g_label = draw.Group( transform = f'translate( { col_scale( c ) }, { inner_height_ + pad } )' )					
	g_label.append( draw.Text( label, font_size,  0, 0, transform = f'rotate( { degrees } )', text_anchor = text_anchor, fill = '#000000' ) )
	g.append( g_label )



def draw_title( g, title, font_size, pad ):
	g.append( draw.Text( title, font_size, ( inner_width_ / 2 ), ( pad ), text_anchor = 'middle', fill = '#000000' ) )



def draw_rows_axis_label( g, label, font_size, pad ):

	g_label = draw.Group( transform = f'translate( { -pad }, { inner_height_ / 2 } )' )					
	g_label.append( draw.Text( label, font_size,  0, 0, transform = 'rotate( -90 )', text_anchor = 'middle', fill = '#000000' ) )
	g.append( g_label  )



def draw_cols_axis_label( g, label, font_size, pad ):
	g.append( draw.Text( label, font_size, ( inner_width_ / 2 ), -( inner_height_ +  pad ), text_anchor = 'middle', fill = '#000000' ) )


import xml.sax.saxutils as xml

class Title( draw.DrawingParentElement ):
    
    TAG_NAME = 'title'
    hasContent = True

    def __init__( self, text, **kwargs ):

    	self.text = text
    	super().__init__( **kwargs )

    def writeContent(self, idGen, isDuplicate, outputFile, dryRun):
        if dryRun:
            return
        outputFile.write( xml.escape( self.text ) )











color_map_category_ = []


color_map_delta_ = []


from matplotlib.colors import LinearSegmentedColormap, to_hex

custom_colors = [ '#F5F5F5', '#303030' ]
linear_grey_scale = LinearSegmentedColormap.from_list( 'custom_linear_grey_scale', custom_colors )

def to_grey( value ):
	return to_hex( linear_grey_scale( value ) )









def col_range_scale( c, alpha, beta, rec_width ):

	c_0 = scale( c, 0, n_cols_, 0, inner_width_ )

	alpha = scale( alpha, col_values_min_[ c ], col_values_max_[ c ], 0, rec_width )
	beta = scale( beta, col_values_min_[ c ], col_values_max_[ c ], 0, rec_width )

	c_p = c_0 + alpha
	rec_width_p = beta - alpha

	return c_p, rec_width_p











def col_delta_scale( c, x_k_f, alpha, beta, rec_width ):

	c_0 = scale( c, 0, n_cols_, 0, inner_width_ )

	x_k_f = scale( x_k_f, col_values_min_[ c ], col_values_max_[ c ], 0, rec_width )

	alpha = scale( alpha, col_values_min_[ c ], col_values_max_[ c ], 0, rec_width )
	beta = scale( beta, col_values_min_[ c ], col_values_max_[ c ], 0, rec_width )

	if x_k_f < alpha:

		c_p = c_0 + x_k_f
		rec_width_p = alpha - x_k_f

	elif x_k_f > beta:

		c_p = c_0 + beta
		rec_width_p = x_k_f - beta

	return c_p, rec_width_p











def draw_range_matrix_legend( g, category_names, pad, info_text = None, rec_width_height = 35, stroke = '#000000', stroke_width = 1, font_size = 16 ):

	for ctg in range( category_names.shape[ 0 ] ):

		fill = color_map_category_[ ctg ]

		g.append( draw.Rectangle( 0 + pad, str( ( ctg * rec_width_height ) ), rec_width_height, rec_width_height, fill = fill, stroke = stroke, stroke_width = stroke_width ) )

		g.append( draw.Text( category_names[ ctg ], font_size, ( pad + ( rec_width_height * 1.2 ) ), -( ( ctg * rec_width_height ) + (rec_width_height / 2 ) + ( font_size / 2 ) ), text_anchor = 'start', fill = '#000000' ) )



	gradient_y_sta = ( category_names.shape[ 0 ] * rec_width_height ) + ( rec_width_height * 1 )
	gradient_y_end = ( category_names.shape[ 0 ] * rec_width_height ) + ( rec_width_height * 6 )

	gradient_x_sta = pad + ( rec_width_height * 1.2 )

	tick_width = 10

	ticks = [ 1.0, 0.75, 0.50, 0.25, 0.0 ]
	n_ticks = len( ticks )
	tick_space = ( gradient_y_end - gradient_y_sta ) / ( n_ticks - 1 )


	gradient = draw.LinearGradient( '0%', '0%', '0%', '100%', gradientUnits = None )
	gradient.addStop( offset = '0%', color = to_grey( 1.0 ) )
	gradient.addStop( offset = '25%', color = to_grey( 0.75 ) )
	gradient.addStop( offset = '50%', color = to_grey( 0.50 ) )
	gradient.addStop( offset = '75%', color = to_grey( 0.25 ) )
	gradient.addStop( offset = '100%', color = to_grey( 0.0 ) )

	
	g.append( draw.Rectangle( 0 + pad, str( gradient_y_sta ), rec_width_height, ( rec_width_height * 5 ), fill = gradient, stroke = stroke, stroke_width = stroke_width ) )

	g.append( draw.Lines( gradient_x_sta, -( gradient_y_sta ), gradient_x_sta, -( gradient_y_end ), stroke = stroke, stroke_width = stroke_width * 1.2 ) )


	for i in range( n_ticks ):

		gradient_y = gradient_y_sta + ( tick_space * i )

		g.append( draw.Lines( gradient_x_sta, -( gradient_y ), gradient_x_sta + tick_width, -( gradient_y ), stroke = stroke, stroke_width = stroke_width * 1.2 ) )

		g.append( draw.Text( str( ticks[ i ] ), font_size, ( pad + ( rec_width_height * 1.6 ) ), -( gradient_y + ( font_size / 4 ) ), text_anchor = 'start', fill = '#000000' ) )



	info_text_y = gradient_y_end + ( rec_width_height )
	
	if info_text is not None:

		g.append( draw.Text( info_text, font_size, ( 0 + pad ), -( info_text_y ), text_anchor = 'start', fill = '#000000' ) )











def draw_rows_left_legend( g, legend, rec_height, title, pad, rec_width = 75, stroke = '#000000', stroke_width = 1, font_size = 16, draw_rows_line = False ):

	title = title.split()
	g.append( draw.Text( title[ 0 ], font_size, -( ( rec_width / 2 ) + pad ), ( 15 + ( font_size * 1.05 ) ), text_anchor = 'middle', fill = '#000000' ) )
	g.append( draw.Text( title[ 1 ], font_size, -( ( rec_width / 2 ) + pad ), ( 15 ), text_anchor = 'middle', fill = '#000000' ) )

	
	for r in range( n_rows_ ):

		value = legend[ r ]

		fill = to_grey( value )
		width = rec_width * value

		g_si = draw.Group()
		g_si.append( Title( text = str( np.round( value, decimals = 2 ) ) ) )

		if draw_rows_line: g_si.append( draw.Rectangle( 0 - rec_width - pad, str( row_scale( r ) ), width, rec_height, shape_rendering = 'crispEdges', fill = fill, stroke = stroke, stroke_width = stroke_width ) )
		else: g_si.append( draw.Rectangle( 0 - rec_width - pad, str( row_scale( r ) ), width, rec_height, shape_rendering = 'crispEdges', fill = fill ) )

		g.append( g_si )


		if draw_rows_line: g.append( draw.Lines( 0 - rec_width - pad, -( row_scale( r ) ), - pad, -( row_scale( r ) ), stroke = stroke, stroke_width = stroke_width ) )


	g.append( draw.Rectangle( 0 - rec_width - pad, '0', rec_width, inner_height_, fill = 'none', stroke = stroke, stroke_width = stroke_width ) )




def draw_rows_right_legend( g, legend, rec_height, title, pad, rec_width = 75, stroke = '#000000', stroke_width = 1, font_size = 16, draw_rows_line = False, draw_change_line = False ):

	title = title.split()

	g.append( draw.Text( title[ 0 ], font_size, ( ( rec_width / 2 ) + pad ), ( 15 + ( font_size * 1.05 ) ), text_anchor = 'middle', fill = '#000000' ) )
	g.append( draw.Text( title[ 1 ], font_size, ( ( rec_width / 2 ) + pad ), ( 15 ), text_anchor = 'middle', fill = '#000000' ) )

	
	if draw_change_line: old_argmax = np.argmax( legend[ 0 ] )

	
	for r in range( n_rows_ ):

		width_sum = 0
		for c in range( legend.shape[ 1 ] ):

			value = legend[ r, c ]
			
			fill = color_map_category_[ c ]
			width = rec_width * value

			g_si = draw.Group()
			g_si.append( Title( text = str( np.round( value, decimals = 2 ) ) ) )

			if draw_rows_line: g_si.append( draw.Rectangle( 0 + pad + width_sum, str( row_scale( r ) ), width, rec_height, shape_rendering = 'crispEdges', fill = fill, stroke = stroke, stroke_width = stroke_width ) )
			else: g_si.append( draw.Rectangle( 0 + pad + width_sum, str( row_scale( r ) ), width, rec_height, shape_rendering = 'crispEdges', fill = fill ) )

			g.append( g_si )

			width_sum += width


		if draw_change_line: 
			argmax = np.argmax( legend[ r ] )
			if old_argmax != argmax:
				old_argmax = argmax
				
				g.append( draw.Lines( ( pad ), -( row_scale( r + 0.5 ) ), rec_width + ( pad ), -( row_scale( r + 0.5 ) ), stroke = stroke, stroke_width = stroke_width * 2 ) )


		if draw_rows_line: g.append( draw.Lines( 0 + pad, -( row_scale( r ) ), rec_width + pad, -( row_scale( r ) ), stroke = stroke, stroke_width = stroke_width ) )



	if not draw_rows_line: g.append( draw.Rectangle( 0 + pad, '0', rec_width, inner_height_, fill = 'none', stroke = stroke, stroke_width = stroke_width ) )











def draw_cols_top_legend( g, legend, rec_width, title, pad, rec_height = 20, stroke = '#000000', stroke_width = 1, font_size = 16, draw_cols_line = False ):

	g.append( draw.Text( title, font_size, ( ( inner_width_ / 2 ) ), ( rec_height + pad + 15 ), text_anchor = 'middle', fill = '#000000' ) )

	
	for c in range( n_cols_ ):

		value = legend[ c ]

		fill = to_grey( value )
		width = rec_width * value

		g_si = draw.Group( transform = f'translate( { col_scale( c ) }, { -( rec_height + pad ) } )' )

		if draw_cols_line: g_si.append( draw.Rectangle( 0, '0', width, rec_height, shape_rendering = 'crispEdges', fill = fill, stroke = stroke, stroke_width = stroke_width ) )
		else: g_si.append( draw.Rectangle( 0, '0', width, rec_height, shape_rendering = 'crispEdges', fill = fill ) )

		g_si.append( Title( text = str( np.round( value, decimals = 2 ) ) ) )
		g.append( g_si )


	g.append( draw.Rectangle( 0, str( -( rec_height + pad ) ), inner_width_, rec_height, fill = 'none', stroke = stroke, stroke_width = stroke_width ) )











def draw_x_lines( g, x_k, rec_width, pad, stroke = '#000000', stroke_width = 2 ):

	for c in range( x_k.shape[ 0 ] ):

		x_k_f = x_k[ c ]

		c_p = col_scale( c + ( scale( x_k_f, col_values_min_[ c ], col_values_max_[ c ], 0, rec_width ) / rec_width ) )

		g_si = draw.Group()
		g_si.append( Title( text = str( np.round( x_k_f, decimals = 2 ) ) ) )
		g_si.append( draw.Lines( c_p, 0, c_p, -inner_height_ - pad, stroke = stroke, stroke_width = stroke_width, stroke_dasharray = '7,14' ) )

		g.append( g_si )











def draw_row_line( g, r, stroke, stroke_width ):
	g.append( draw.Lines( 0, -( row_scale( r ) ), inner_width_, -( row_scale( r ) ), stroke = stroke, stroke_width = stroke_width ) )


def draw_col_line( g, c, stroke, stroke_width ):
	g.append( draw.Lines( col_scale( c ), 0, col_scale( c ), -inner_height_, stroke = stroke, stroke_width = stroke_width ) )








# color_map_category = [ '#1f77b3', '#ff7e0e', '#bcbc21', '#8c564b', '#9367bc', '#e277c1', '#ffdb00', '#8a2844', '#00aa79', '#aa3baf', '#d89c00', '#a3a39e', '#3f69ff', '#46490c', '#7b6985', '#6b978c', '#ff9a75', '#835bff', '#7c6b46', '#80b654', '#bc0049', '#fd93ff', '#5d0018', '#89d1d1', '#9c8cd3' ], 
# 	color_map_delta = [ '#2ca02c', '#d62728' ] 

# color_map_category = [ '#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf' ], 
# 	color_map_delta = [ '#377eb8', '#e41a1c' ]


def draw_range_matrix( matrix, col_values_min, col_values_max, matrix_row_categories, category_names, rows_left_legend, rows_left_legend_title, rows_right_legend_1, rows_right_legend_1_title, cols_top_legend, cols_top_legend_title, rows_right_legend_2 = None, rows_right_legend_2_title = None, x_k = None, draw_x_k = False, draw_deltas = False, info_text = None, draw_change_line = False,

	width = 2160, height = 1080, margin_top = 125, margin_right = 550, margin_bottom = 100, margin_left = 300, font_size = 25,

	title = None, title_font_size = 25, title_pad = 30,

	rows_axis_label = None, rows_axis_label_font_size = None, pad_row_axis_label = 175, row_labels = None, row_label_font_size = None, pad_row_label = 15, draw_rows_line = False,

	cols_axis_label = None, cols_axis_label_font_size = None, pad_col_axis_label = 115, col_labels = None, col_label_degrees = 0, col_label_font_size = None, pad_col_label = 50, draw_cols_line = False,

	background = '#ffffff', cell_background = False, stroke = '#000000', stroke_width = 2,

	color_map_category = [ '#1f77b3', '#ff7e0e', '#bcbc21', '#8c564b', '#9367bc', '#e277c1', '#ffdb00', '#8a2844', '#00aa79', '#aa3baf', '#d89c00', '#a3a39e', '#3f69ff', '#46490c', '#7b6985', '#6b978c', '#ff9a75', '#835bff', '#7c6b46', '#80b654', '#bc0049', '#fd93ff', '#5d0018', '#89d1d1', '#9c8cd3' ], 
	color_map_delta = [ '#4daf4a','#984ea3' ] ):


	global n_rows_ , n_cols_, margin_top_, margin_right_, margin_bottom_, margin_left_, inner_width_, inner_height_, col_values_max_, col_values_min_, color_map_category_, color_map_delta_


	if rows_axis_label_font_size is None: rows_axis_label_font_size = font_size
	if row_label_font_size is None: row_label_font_size = font_size
	if cols_axis_label_font_size is None: cols_axis_label_font_size = font_size
	if col_label_font_size is None: col_label_font_size = font_size

	
	color_map_category_ = color_map_category
	color_map_delta_ = color_map_delta


	n_rows_ = matrix.shape[ 0 ]
	n_cols_ = int( matrix.shape[ 1 ] / 2 )


	col_values_max_ = col_values_max
	col_values_min_ = col_values_min


	margin_top_ = margin_top
	margin_right_= margin_right
	margin_bottom_ = margin_bottom
	margin_left_ = margin_left


	inner_width_ = width - margin_right_ - margin_left_
	inner_height_ = height - margin_top_ - margin_bottom_

	rec_width = inner_width_ / n_cols_
	rec_height = inner_height_ / n_rows_




	d = draw.Drawing( width, height, origin = ( 0, -height ) ) # bug - use arg y as string, except for text ??
	if background is not None: d.append( draw.Rectangle( 0, '0', width, height, fill = background ) ) # background

	g_matrix = draw.Group( transform = f'translate( { margin_left_ }, { margin_top_ } )' )





	for r in range( n_rows_ ):		

		for c in range( n_cols_ ):

			a = c * 2
			b = a + 1

			alpha = matrix[ r, a ]
			beta = matrix[ r, b ]

			if ( alpha != 0.0 ) or ( beta != 0.0 ):

				
				if not draw_deltas:

					fill = color_map_category_[ matrix_row_categories[ r ] ]
					rect_info = '[ ' + str( np.round( alpha, decimals = 2 ) ) + ', ' + str( np.round( beta, decimals = 2 ) ) + ' ]'
					rect_background_info = '[ ' + str( np.round( col_values_min_[ c ], decimals = 2 ) ) + ', ' + str( np.round( col_values_max_[ c ], decimals = 2 ) ) + ' ]'

					g_si = draw.Group()
					g_si.append( Title( text = rect_background_info ) )

					if cell_background: g_si.append( draw.Rectangle( col_scale( c ), str( row_scale( r ) ), rec_width, rec_height, shape_rendering = 'crispEdges', fill = fill, stroke = 'none', opacity = 0.25 ) )
					else: g_si.append( draw.Rectangle( col_scale( c ), str( row_scale( r ) ), rec_width, rec_height, shape_rendering = 'crispEdges', fill = '#ffffff', stroke = 'none' ) )

					g_matrix.append( g_si )				

					

					c_p, rec_width_p = col_range_scale( c, matrix[ r, a ], matrix[ r, b ], rec_width )

					g_si = draw.Group()
					g_si.append( Title( text = rect_info ) )
					g_si.append( draw.Rectangle( c_p, str( row_scale( r ) ), rec_width_p, rec_height, shape_rendering = 'crispEdges', fill = fill, stroke = 'none' ) )
					g_matrix.append( g_si )


				elif ( x_k[ c ] < alpha ) or ( x_k[ c ] > beta ):

					x_k_f = x_k[ c ]
					c_p, rec_width_p = col_delta_scale( c, x_k_f, alpha, beta, rec_width )

					if x_k_f < alpha:

						fill = color_map_delta_[ 0 ]
						rect_info = str( np.round( alpha - x_k_f, decimals = 2 ) )						

					elif x_k_f > beta:

						fill = color_map_delta_[ 1 ]
						rect_info = str( np.round( beta - x_k_f, decimals = 2 ) )


					if cell_background: g_matrix.append( draw.Rectangle( col_scale( c ), str( row_scale( r ) ), rec_width, rec_height, shape_rendering = 'crispEdges', fill = fill, stroke = 'none', opacity = 0.25 ) ) # cell background

					g_si = draw.Group()
					g_si.append( Title( text = rect_info ) )
					g_si.append( draw.Rectangle( c_p, str( row_scale( r ) ), rec_width_p, rec_height, shape_rendering = 'crispEdges', fill = fill, stroke = 'none' ) )
					g_matrix.append( g_si )





	pad = 30
	pad_row_label += 75 + pad





	if title is not None: draw_title( g_matrix, title, title_font_size, title_pad )
	if rows_axis_label is not None: draw_rows_axis_label( g_matrix, rows_axis_label, font_size = rows_axis_label_font_size, pad = pad_row_axis_label )
	if cols_axis_label is not None: draw_cols_axis_label( g_matrix, cols_axis_label, font_size = cols_axis_label_font_size, pad = pad_col_axis_label )





	g_matrix.append( draw.Rectangle( 0, str( 0 ), inner_width_, inner_height_, fill = 'none', stroke = stroke, stroke_width = stroke_width ) ) # matrix box frame




	if ( row_labels is not None ) or draw_rows_line: 
		for r in range( n_rows_ ): 
			
			if row_labels is not None: draw_row_label( g_matrix, r, row_labels[ r ], font_size = row_label_font_size, rec_height = rec_height, pad = pad_row_label )

			if draw_rows_line and ( r <= n_rows_ - 2 ): draw_row_line( g_matrix, r + 1, stroke, stroke_width )


	if ( col_labels is not None ) or draw_cols_line: 
		for c in range( n_cols_ ):

			if col_labels is not None: 

				if ( x_k is not None ) and draw_x_k:
					
					c_p = c + ( scale( x_k[ c ], col_values_min_[ c ], col_values_max_[ c ], 0, rec_width ) / rec_width )
					draw_col_label( g_matrix, c_p, col_labels[ c ], col_label_font_size, col_label_degrees, pad = pad_col_label )

				else: draw_col_label( g_matrix, ( c + 0.5 ), col_labels[ c ], col_label_font_size, col_label_degrees, pad = pad_col_label )

			if draw_cols_line and ( c <= n_cols_ - 2 ): draw_col_line( g_matrix, c + 1, stroke, stroke_width )





	if ( x_k is not None ) and draw_x_k: draw_x_lines( g_matrix, x_k, rec_width, pad_col_label - pad, stroke_width = stroke_width * 1.7 )
	




	g_left_legend = draw.Group( transform = f'translate( { margin_left_ }, { margin_top_ } )' )
	draw_rows_left_legend( g_left_legend, rows_left_legend, rec_height, rows_left_legend_title, pad = pad, draw_rows_line = draw_rows_line, font_size = font_size, stroke_width = stroke_width )




	g_top_legend = draw.Group( transform = f'translate( { margin_left_ }, { margin_top_ } )' )
	if cols_top_legend is not None: draw_cols_top_legend( g_top_legend, cols_top_legend, rec_width, title = cols_top_legend_title, pad = pad, draw_cols_line = draw_cols_line, font_size = font_size, stroke_width = stroke_width )




	g_right_legend = draw.Group( transform = f'translate( { margin_left_ + inner_width_ }, { margin_top_ } )' )
	draw_rows_right_legend( g_right_legend, rows_right_legend_1, rec_height, rows_right_legend_1_title, pad = pad, draw_rows_line = draw_rows_line, font_size = font_size, stroke_width = stroke_width )
	pad += 95

	if rows_right_legend_2 is not None: 

		pad += 25
		draw_rows_right_legend( g_right_legend, rows_right_legend_2, rec_height, rows_right_legend_2_title, pad = pad, draw_rows_line = draw_rows_line, draw_change_line = draw_change_line, font_size = font_size, stroke_width = stroke_width )
		pad += 95



	pad += 45
	draw_range_matrix_legend( g_right_legend, category_names, info_text = info_text, pad = pad, font_size = font_size, stroke_width = stroke_width )	
	

	

	d.append( g_matrix )

	d.append( g_left_legend )
	d.append( g_right_legend )
	d.append( g_top_legend )

	return d