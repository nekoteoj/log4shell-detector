package com.nekoteoj.vulnerableserver;

import io.javalin.Javalin;
import org.apache.logging.log4j.*;
import org.apache.logging.log4j.core.config.*;

/**
 * Hello world!
 *
 */
public class App {

    private static final Logger logger = LogManager.getLogger("App");

    public static void main(String[] args) {
        Configurator.initialize(new DefaultConfiguration());
        Configurator.setRootLevel(Level.INFO);
        Javalin app = Javalin.create().start(3000);
        app.get("/", ctx -> {
            String userAgent = ctx.header("User-Agent");
            logger.info("Client's user agent: " + userAgent);
            ctx.result("Hello, World");
        });
    }

}
