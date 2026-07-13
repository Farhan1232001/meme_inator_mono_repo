# Makefile for creating Django apps with layered structure
# -------------------------------------------------------
# Usage:
#   make app APP_NAME=<app_name>
# Example:
#   make app APP_NAME=auth
#   make app APP_NAME=feeds
#   make app APP_NAME=posts
# -------------------------------------------------------

.PHONY: app

# Target to create a new Django app
app:
ifndef APP_NAME
	$(error APP_NAME is undefined. Usage: make app APP_NAME=<app_name>)
endif

	@echo "Creating Django app: $(APP_NAME)"

	# Create Django app
	python manage.py startapp $(APP_NAME)

	# Move the newly created app into the apps/ directory
	mv $(APP_NAME) apps/

	# Create the layered folder structure based on Clean Architecture principles:
	# 1. Core Layers
	mkdir -p apps/$(APP_NAME)/application
	mkdir -p apps/$(APP_NAME)/domain
	mkdir -p apps/$(APP_NAME)/infrastructure

	# 2. Application Subdirectories
	mkdir -p apps/$(APP_NAME)/application/delivery
	mkdir -p apps/$(APP_NAME)/application/orchestration
	mkdir -p apps/$(APP_NAME)/application/usecases
	mkdir -p apps/$(APP_NAME)/application/dtos

	# 3. Domain Subdirectories
	mkdir -p apps/$(APP_NAME)/domain/entities
	mkdir -p apps/$(APP_NAME)/domain/irepositories
	mkdir -p apps/$(APP_NAME)/domain/iusecases

	# 4. Data (Infrastructure) Subdirectories
	mkdir -p apps/$(APP_NAME)/infrastructure/models
	mkdir -p apps/$(APP_NAME)/infrastructure/repositories
	# mkdir -p apps/$(APP_NAME)/infrastructure/services
	mkdir -p apps/$(APP_NAME)/infrastructure/caches
	mkdir -p apps/$(APP_NAME)/infrastructure/queues

	# Add __init__.py so the app and its sub-packages are recognized by Python
	touch apps/$(APP_NAME)/__init__.py
	touch apps/$(APP_NAME)/application/__init__.py
	touch apps/$(APP_NAME)/application/delivery/__init__.py
	touch apps/$(APP_NAME)/application/orchestration/__init__.py
	touch apps/$(APP_NAME)/domain/__init__.py
	touch apps/$(APP_NAME)/domain/entities/__init__.py
	touch apps/$(APP_NAME)/domain/irepositories/__init__.py
	touch apps/$(APP_NAME)/domain/usecases/__init__.py
	touch apps/$(APP_NAME)/infrastructure/__init__.py
	touch apps/$(APP_NAME)/infrastructure/models/__init__.py
	touch apps/$(APP_NAME)/infrastructure/repositories/__init__.py
	# touch apps/$(APP_NAME)/infrastructure/services/__init__.py
	touch apps/$(APP_NAME)/infrastructure/caches/__init__.py
	touch apps/$(APP_NAME)/infrastructure/queues/__init__.py

	# Remove the default views.py file, since we are structuring apps differently
	# rm -f apps/$(APP_NAME)/views.py
	rm -f apps/$(APP_NAME)/models.py
	rm -f apps/$(APP_NAME)/tests.py
	rm -f apps/$(APP_NAME)/admin.py

	@echo "App $(APP_NAME) created with full layered structure."