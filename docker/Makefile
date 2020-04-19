demo :
	# *******************************
	# First Request, main information
	# *******************************
	http localhost:8000/rates
	# **********************************
	# Second Request, Web service status
	# **********************************
	http localhost:8000/rates/status
	# ********************************************
	# Third Request, Base change, main information
	# ********************************************
	http localhost:8000/rates base==USD
	# *********************************************************
	# Fourth Request, Consulting of two bases, error simulation
	# *********************************************************
	http localhost:8000/rates base==USD base==GBP
	# *********************************
	# Fifth Request, Web service status
	# *********************************
	http localhost:8000/rates/status
	# *******************************************
	# Sixth Request, Info consulting, Symbols=JPY
	# *******************************************
	http localhost:8000/rates/info symbols==JPY
	# ***********************************
	# Seventh Request, Web service status
	# ***********************************
	http localhost:8000/rates/status
	# ************************************************
	# Eighth Request, Info Consulting, error simulation
	# ************************************************
	http localhost:8000/rates/info symbols==bvp
	# *********************************
	# Ninth Request, Web service status
	# *********************************
	http localhost:8000/rates/status
	# **********************************************************
	# Tenth Request, Info Consulting, Base=CZK, Symbols=EUR,USD
	# **********************************************************
	http localhost:8000/rates/info base==CZK symbols==eur symbols==USD
	# *********************************
	# Final Request, Web service status
	# *********************************
	http localhost:8000/rates/status

docker:
	sudo docker run --rm -it --network="host" my-demo
