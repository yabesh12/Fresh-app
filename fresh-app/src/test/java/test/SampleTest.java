// package karate;
//
// import com.intuit.karate.junit5.Karate;
//
// class SampleTest {
//
//     @Karate.Test
//     Karate testSample() {
//         return Karate.run("sample").relativeTo(getClass());
//     }
//
//     @Karate.Test
//     Karate testTags() {
//         return Karate.run("tags").tags("@second").relativeTo(getClass());
//     }
//
//     @Karate.Test
//     Karate testSystemProperty() {
//         return Karate.run("classpath:test/features/create_route.feature");
//     }
// }
//
//
//
// package test;
//
// import com.intuit.karate.junit5.Karate;
//
// class SampleTest {
//
//     @Karate.Test
//     Karate testSample() {
//         return Karate.run().relativeTo(getClass());
//     }
// }



import com.intuit.karate.KarateOptions;
import com.intuit.karate.junit5.Karate;

@KarateOptions(tags = {"@debug"})
// How to Run it - mvn clean test "-Dkarate.options=--tags @debug"
class SampleTest {

    // this will run all *.feature files that exist in sub-directories
    // see https://¬github.com/intuit/karate#naming-conventions
    @Karate.Test
    Karate testSample() {
        return Karate.run().relativeTo(getClass());
    }
}

