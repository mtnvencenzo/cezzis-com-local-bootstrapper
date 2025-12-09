from injector import Injector

from cezzis_com_bootstrapper.app_module import AppModule


def create_injector() -> Injector:
    return Injector([AppModule()])


def main():
    """Main entry point for bootstrapping."""
    # injector = create_injector()

    # TODO: Add your bootstrapping tasks here:
    # - Initialize queues
    # - Setup blob storage
    # - Initialize database
    # - Seed data

    print("Bootstrapping completed successfully")


if __name__ == "__main__":
    main()

# app = FastAPI()

# app.include_router(injector.get(SemanticSearchRouter))
# app.include_router(injector.get(ConverstionalSearchRouter))
